import razorpay
import hmac
import hashlib
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from config.database import execute_query
from config.settings import settings
from middleware.auth import get_current_user, get_optional_user
from datetime import datetime
import time

router = APIRouter(prefix="/payments", tags=["Payments"])

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


class CreateOrderRequest(BaseModel):
    amount: float
    description: str | None = "Service Payment"
    project_id: str | None = None


class VerifyPaymentRequest(BaseModel):
    razorpay_payment_id: str
    razorpay_order_id: str | None = None
    razorpay_signature: str | None = None
    amount: float | None = None


@router.post("/create-order")
async def create_order(data: CreateOrderRequest, current_user=Depends(get_optional_user)):
    db = get_db()
    try:
        # Create Razorpay order
        amount_paise = int(data.amount * 100)
        receipt = f"rcpt_{int(time.time())}"

        order_data = {
            "amount": amount_paise,
            "currency": "INR",
            "receipt": receipt,
            "notes": {
                "description": data.description,
                "user_id": current_user["id"] if current_user else "guest",
                "project_id": data.project_id if data.project_id else None
            }
        }

        order = razorpay_client.order.create(data=order_data)

        # Store payment record
        user_id = current_user["id"] if current_user else None
        execute_query(
            """
            INSERT INTO payments 
            (user_id, project_id, gateway_order_id, amount, currency, status, metadata) 
            VALUES (%s, %s, %s, %s, %s, 'created', %s)
            """,
            (user_id, data.project_id, order["id"], data.amount, "INR", f'{{"description": "{data.description}", "receipt": "{receipt}"}}')
        )

        return {
            "order_id": order["id"],
            "amount": amount_paise,
            "currency": "INR",
            "key_id": settings.RAZORPAY_KEY_ID,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create order: {str(e)}")


@router.post("/verify")
async def verify_payment(data: VerifyPaymentRequest, current_user=Depends(get_optional_user)):
    db = get_db()
    try:
        # Verify signature if provided
        if data.razorpay_order_id and data.razorpay_signature:
            generated_signature = hmac.new(
                settings.RAZORPAY_KEY_SECRET.encode(),
                f"{data.razorpay_order_id}|{data.razorpay_payment_id}".encode(),
                hashlib.sha256
            ).hexdigest()

            if generated_signature != data.razorpay_signature:
                # Update payment status to failed
                await db.payments.update_one(
                    {"razorpay_order_id": data.razorpay_order_id},
                    {"$set": {"status": "failed", "updated_at": datetime.utcnow()}}
                )
                raise HTTPException(status_code=400, detail="Payment verification failed")

        # Update payment record
        if data.razorpay_order_id:
            execute_query(
                "UPDATE payments SET gateway_payment_id = %s, status = 'completed' WHERE gateway_order_id = %s",
                (data.razorpay_payment_id, data.razorpay_order_id)
            )
        else:
            # Direct payment without order
            user_id = current_user["id"] if current_user else None
            execute_query(
                "INSERT INTO payments (user_id, gateway_payment_id, amount, status) VALUES (%s, %s, %s, 'completed')",
                (user_id, data.razorpay_payment_id, data.amount or 0)
            )

        # If it was a project purchase, record ownership
        if data.razorpay_order_id:
            payment = execute_query("SELECT * FROM payments WHERE gateway_order_id = %s", (data.razorpay_order_id,), fetch_one=True)
            if payment and payment.get("project_id") and payment.get("user_id"):
                execute_query(
                    "INSERT INTO user_projects (user_id, project_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (payment["user_id"], payment["project_id"])
                )

        return {"message": "Payment verified successfully", "payment_id": data.razorpay_payment_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification error: {str(e)}")


@router.get("")
async def get_payments(current_user=Depends(get_current_user)):
    payments = execute_query("SELECT * FROM payments WHERE user_id = %s ORDER BY created_at DESC", (current_user["id"],), fetch_all=True)
    return {"payments": payments}


@router.put("/{payment_id}")
async def update_payment_status(payment_id: int, current_user=Depends(get_current_user)):
    result = execute_query(
        "UPDATE payments SET status = 'completed' WHERE id = %s RETURNING *",
        (payment_id,),
        fetch_one=True
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Payment not found")
        
    return {"message": "Payment status updated", "payment": result}
