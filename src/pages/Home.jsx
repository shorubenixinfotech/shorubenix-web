import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  ArrowRight, Code2, Smartphone, Cloud, Shield, Zap, Globe,
  CheckCircle2, Star, Users, Award, TrendingUp, Play
} from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import ServiceDetailsModal from '../components/ServiceDetailsModal'

const fadeInUp = {
  initial: { opacity: 0, y: 30 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true },
  transition: { duration: 0.6 }
}

const staggerContainer = {
  initial: {},
  whileInView: { transition: { staggerChildren: 0.1 } },
  viewport: { once: true }
}

const services = [
  {
    icon: Code2, title: 'Web Development',
    desc: 'Enterprise-grade web applications and high-performance corporate websites.',
    longDesc: 'Our web development team crafts high-performance, secure, and scalable digital solutions tailored for enterprises. We specialize in robust backend architectures and lightning-fast frontend experiences.',
    features: ['Custom Web Applications', 'React & Next.js Ecosystem', 'Full-stack Architectures', 'Performance Optimization', 'Post-launch Support'],
    color: 'from-sky-500 to-blue-500'
  },
  {
    icon: Smartphone, title: 'Mobile Apps',
    desc: 'Secure and scalable mobile solutions for iOS and Android platforms.',
    longDesc: 'From native experiences to cross-platform brilliance, we build mobile applications that resonate with users. Our focus is on seamless performance, intuitive UX, and secure data handling.',
    features: ['Native iOS & Android', 'React Native Development', 'App Store Optimization', 'Third-party Integrations', 'Real-time Features'],
    color: 'from-blue-600 to-indigo-600'
  },
  {
    icon: Cloud, title: 'Cloud Solutions',
    desc: 'Advanced cloud architecture, migration, and optimized infrastructure.',
    longDesc: 'Scale with confidence using our cloud expertise. We provide end-to-end cloud strategy, seamless migration, and continuous infrastructure optimization to ensure maximum uptime and cost-efficiency.',
    features: ['AWS & Azure Strategy', 'Cloud Migration Services', 'Infrastructure as Code (IaC)', 'Auto-scaling & Resilience', 'Cost-optimization Audits'],
    color: 'from-slate-700 to-slate-900'
  },
  {
    icon: Shield, title: 'Cyber Security',
    desc: 'Military-grade protection for your digital assets and business operations.',
    longDesc: 'In an era of rising digital threats, we provide comprehensive cybersecurity services to protect your core assets. From penetration testing to security framework implementation, we keep your business safe.',
    features: ['Penetration Testing', 'Identity & Access Management', 'Vulnerability Assessments', 'Security Audits', 'Compliance Consulting'],
    color: 'from-slate-800 to-black'
  },
  {
    icon: Zap, title: 'Technical Guidance',
    desc: 'Strategic IT consulting and end-to-end project management.',
    longDesc: 'Align your technology with your business goals. Our consultants provide the strategic oversight and technical expertise needed to navigate complex digital transformations successfully.',
    features: ['IT Strategy Consulting', 'Architecture Planning', 'Technical Feasibility Studies', 'Vendor Management', 'Resource Planning'],
    color: 'from-sky-400 to-sky-600'
  },
  {
    icon: Globe, title: 'Digital Solutions',
    desc: 'Innovative IoT projects and smart automation for modern businesses.',
    longDesc: 'We bridge the gap between hardware and software with innovative IoT and automation solutions. We help businesses leverage real-time data to drive efficiency and unlock new opportunities.',
    features: ['IoT Ecosystem Design', 'Business Automation', 'Real-time Monitoring', 'Smart Hardware Integration', 'Data Analytics Platforms'],
    color: 'from-blue-500 to-sky-500'
  },
]

const stats = [
  { icon: Users, value: '250+', label: 'Corporate Clients' },
  { icon: Award, value: '300+', label: 'Projects Completed' },
  { icon: Star, value: '4.9', label: 'Satisfaction Rate' },
  { icon: TrendingUp, value: '24/7', label: 'Expert Support' },
]

const testimonials = [
  { name: 'Shobika', role: 'Director, TechGlobal', text: 'Shorubenix provided an exceptional enterprise solution that streamlined our entire operation. Truly a professional team.', rating: 5 },
  { name: 'Ruban Raj', role: 'Founder, InnovateHQ', text: 'The attention to detail and technical precision delivered by Shorubenix is outstanding. Highly recommended for corporate projects.', rating: 5 },
  { name: 'Johnsonselva', role: 'CTO, DataSystems', text: 'Innovative, reliable, and affordable. They are our go-to partner for all cloud and web infrastructure needs.', rating: 5 },
]

export default function Home() {
  const { isAuthenticated, isAdminAuthenticated } = useAuth()
  const navigate = useNavigate()
  const [serviceForModal, setServiceForModal] = useState(null)
  const [isModalOpen, setIsModalOpen] = useState(false)

  useEffect(() => {
    if (isAdminAuthenticated) {
      navigate('/admin', { replace: true })
    }

  }, [isAuthenticated, isAdminAuthenticated, navigate])

  const handleOpenModal = (service) => {
    setServiceForModal(service)
    setIsModalOpen(true)
  }

  return (
    <div className="overflow-hidden grain">
      {/* Hero Section */}
      <section className="relative min-h-[90vh] flex items-center section-padding pt-32 lg:pt-40">
        {/* Background Image with Overlay */}
        <div className="absolute inset-0 z-0">
          <img
            src="/office-bg.png"
            alt="Office Background"
            className="w-full h-full object-cover opacity-40 scale-105"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-[#030712]/10 via-[#030712]/80 to-[#030712]" />
          <div className="absolute inset-0 bg-[#030712]/20 backdrop-blur-[2px]" />

          {/* Animated Glows */}
          <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-sky-500/10 rounded-full blur-[120px] animate-pulse-slow" />
          <div className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-blue-600/10 rounded-full blur-[120px] animate-pulse-slow" style={{ animationDelay: '2s' }} />
        </div>

        <div className="container-custom relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8 }}
            >
              <span className="inline-flex items-center gap-2 px-5 py-2 rounded-full bg-white/5 border border-white/10 text-sky-400 text-sm font-semibold mb-8 backdrop-blur-md">
                <Zap className="w-4 h-4" />
                <span className="tracking-wider uppercase">Future-Proof Digital Solutions</span>
              </span>
              <h1 className="text-5xl sm:text-6xl lg:text-8xl font-display font-bold leading-[1.1] mb-8 tracking-tight">
                Empowering <span className="gradient-text-blue">Innovation</span> <br />
                Through <span className="text-white">Technology</span>
              </h1>
              <p className="text-xl text-slate-400 mb-12 max-w-2xl mx-auto leading-relaxed font-light">
                Shorubenix Info Technology delivers high-precision technical solutions.
                From professional Web Development to smart IoT Projects and Academic Support.
              </p>

              <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
                <Link to="/contact" className="btn-primary flex items-center gap-3 group w-full sm:w-auto justify-center">
                  Start Consultation
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </Link>
                <Link to="/portfolio" className="btn-secondary flex items-center gap-3 w-full sm:w-auto justify-center">
                  <Play className="w-5 h-5 text-sky-500" />
                  Browse Themes
                </Link>
              </div>

              <div className="mt-20 flex flex-wrap items-center justify-center gap-12 opacity-50 grayscale hover:grayscale-0 transition-all duration-700">
                <div className="text-2xl font-bold font-display tracking-tighter text-slate-500">MICROSOFT</div>
                <div className="text-2xl font-bold font-display tracking-tighter text-slate-500">ADOBE</div>
                <div className="text-2xl font-bold font-display tracking-tighter text-slate-500">AMAZON</div>
                <div className="text-2xl font-bold font-display tracking-tighter text-slate-500">GOOGLE</div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="section-padding bg-[#030712]/50 relative border-y border-white/5">
        <div className="container-custom">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, i) => (
              <motion.div
                key={stat.label}
                {...fadeInUp}
                transition={{ delay: i * 0.1 }}
                className="text-center group"
              >
                <div className="text-4xl lg:text-5xl font-display font-black text-white mb-2 group-hover:scale-110 transition-transform">
                  {stat.value}
                </div>
                <p className="text-slate-500 text-sm font-semibold tracking-widest uppercase">{stat.label}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="section-padding relative overflow-hidden">
        <div className="container-custom relative z-10">
          <motion.div {...fadeInUp} className="text-center mb-20">
            <h2 className="text-4xl md:text-5xl lg:text-6xl font-display font-bold mb-6">
              Expert <span className="gradient-text-blue">IT Services</span>
            </h2>
            <p className="text-slate-400 max-w-2xl mx-auto text-lg font-light leading-relaxed">
              We provide high-end technological consulting and implementation at an affordable scale,
              ensuring your digital success with precision and quality.
            </p>
          </motion.div>

          <motion.div {...staggerContainer} className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {services.map((service, i) => (
              <motion.div key={service.title} {...fadeInUp} transition={{ delay: i * 0.1 }}>
                <div className="glass-card p-10 h-full group border-white/[0.03] hover:border-sky-500/30">
                  <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${service.color} p-[1px] mb-8`}>
                    <div className="w-full h-full rounded-2xl bg-[#030712] flex items-center justify-center group-hover:bg-transparent transition-all duration-500">
                      <service.icon className="w-8 h-8 text-white group-hover:scale-110 transition-transform" />
                    </div>
                  </div>
                  <h3 className="text-2xl font-display font-bold text-white mb-4">{service.title}</h3>
                  <p className="text-slate-400 leading-relaxed font-light mb-8">{service.desc}</p>
                  <button
                    onClick={() => handleOpenModal(service)}
                    className="pt-6 border-t border-white/5 w-full flex items-center text-sky-400 text-sm font-bold tracking-widest uppercase group-hover:text-white transition-colors"
                  >
                    View Details <ArrowRight className="w-4 h-4 ml-3 group-hover:translate-x-2 transition-transform" />
                  </button>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Corporate Features */}
      <section className="section-padding bg-slate-900/10 border-y border-white/5">
        <div className="container-custom">
          <div className="grid lg:grid-cols-2 gap-20 items-center">
            <motion.div {...fadeInUp}>
              <h2 className="text-4xl md:text-5xl font-display font-bold mb-8 leading-tight">
                Professionalism Met with <br />
                <span className="gradient-text-blue">Practical Implementation</span>
              </h2>
              <p className="text-slate-400 mb-10 text-xl font-light leading-relaxed">
                At Shorubenix, we combine creative excellence with technical rigor to deliver solutions
                that actually move the needle for your business or academic career.
              </p>
              <div className="grid sm:grid-cols-2 gap-6">
                {[
                  'Enterprise Tech Stack',
                  'Affordable Pricing',
                  'End-to-End Support',
                  'Academic Precision',
                  'Real-world IoT',
                  'Verified Quality'
                ].map((item) => (
                  <div key={item} className="flex items-center gap-4 p-4 rounded-xl bg-white/[0.02] border border-white/[0.05]">
                    <CheckCircle2 className="w-6 h-6 text-sky-500 flex-shrink-0" />
                    <span className="text-slate-300 font-medium">{item}</span>
                  </div>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="relative p-1 bg-gradient-to-br from-sky-500/20 to-transparent rounded-[2.5rem]"
            >
              <div className="glass-card p-12 overflow-hidden relative">
                <div className="absolute top-0 right-0 w-64 h-64 bg-sky-500/10 rounded-full blur-[80px]" />
                <div className="text-sky-400 text-6xl font-display font-black mb-8 opacity-20">2026</div>
                <h3 className="text-3xl font-display font-bold text-white mb-6">Leading the Digital Transformation</h3>
                <p className="text-slate-400 mb-10 leading-relaxed font-light">
                  Our approach ensures that every project — whether a simple website or a complex IoT ecosystem — is built with a focus on long-term scalability and reliability.
                </p>
                <div className="flex items-center gap-8">
                  <div>
                    <div className="text-3xl font-bold text-white">100%</div>
                    <div className="text-sm text-slate-500 uppercase tracking-widest font-bold">Secure</div>
                  </div>
                  <div className="h-10 w-px bg-white/10" />
                  <div>
                    <div className="text-3xl font-bold text-white">50+</div>
                    <div className="text-sm text-slate-500 uppercase tracking-widest font-bold">Tools</div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="section-padding">
        <div className="container-custom">
          <motion.div {...fadeInUp} className="text-center mb-20">
            <h2 className="text-4xl md:text-5xl font-display font-bold mb-6">
              Client <span className="gradient-text-blue">Success Stories</span>
            </h2>
          </motion.div>
          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((t, i) => (
              <motion.div key={t.name} {...fadeInUp} transition={{ delay: i * 0.1 }}>
                <div className="glass-card p-10 h-full flex flex-col border-white/[0.03]">
                  <div className="flex gap-2 mb-8">
                    {[...Array(t.rating)].map((_, j) => (
                      <Star key={j} className="w-5 h-5 text-sky-400 fill-sky-400" />
                    ))}
                  </div>
                  <p className="text-slate-300 text-lg italic leading-relaxed mb-10 flex-1 font-light">&ldquo;{t.text}&rdquo;</p>
                  <div className="flex items-center gap-5 pt-8 border-t border-white/5">
                    <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-slate-700 to-slate-900 flex items-center justify-center text-white font-black text-xl shadow-xl shadow-black/50">
                      {t.name.charAt(0)}
                    </div>
                    <div>
                      <p className="text-white font-bold text-lg">{t.name}</p>
                      <p className="text-slate-500 text-xs font-bold tracking-widest uppercase">{t.role}</p>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <ServiceDetailsModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        service={serviceForModal}
      />
    </div>
  )
}
