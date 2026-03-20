import { motion } from 'framer-motion'
import { Users, Target, Lightbulb, Heart, Award, Clock, Code2, Globe, Cpu, BookOpen, GraduationCap } from 'lucide-react'

const fadeInUp = {
  initial: { opacity: 0, y: 30 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true },
  transition: { duration: 0.6 }
}

const timeline = [
  { year: '2022', title: 'The Beginning', desc: 'Shorubenix Info Technology was born with a bold vision to ignite innovation.' },
  { year: '2023', title: 'Expanding Horizons', desc: 'Started providing comprehensive Academic Project Support and IoT solutions.' },
  { year: '2024', title: 'Digital Excellence', desc: 'Automating business challenges and building careers through technical guidance.' },
]

export default function About() {
  return (
    <div className="pt-20">
      {/* Hero */}
      <section className="section-padding">
        <div className="container-custom">
          <motion.div {...fadeInUp} className="text-center max-w-4xl mx-auto">
            <span className="inline-block px-4 py-1.5 rounded-full bg-primary-500/10 border border-primary-500/20 text-primary-300 text-sm mb-4">
              Our Story
            </span>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-display font-bold mb-6">
              Transforming Challenges into <span className="gradient-text">Smart Digital Solutions</span>
            </h1>
            <p className="text-dark-300 text-lg leading-relaxed mb-8">
              Founded in 2022, Shorubenix Info Technology was born with a bold vision — to ignite innovation and empower ideas through technology.
            </p>
            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 text-left">
              {[
                { icon: Code2, title: 'Web Development', desc: 'Professional & modern web apps.' },
                { icon: GraduationCap, title: 'Academic Support', desc: 'Complete project guidance.' },
                { icon: Cpu, title: 'IoT Projects', desc: 'Innovative hardware solutions.' },
                { icon: BookOpen, title: 'Project Reports', desc: 'Well-structured documentation.' },
              ].map((item, i) => (
                <motion.div key={item.title} {...fadeInUp} transition={{ delay: i * 0.1 }} className="glass-card p-5 border-white/5">
                  <item.icon className="w-6 h-6 text-primary-400 mb-3" />
                  <h4 className="text-white font-semibold mb-1 text-sm">{item.title}</h4>
                  <p className="text-dark-400 text-xs">{item.desc}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Main Content */}
      <section className="section-padding pt-0">
        <div className="container-custom">
          <motion.div {...fadeInUp} className="glass-card p-10 mb-12 border-primary-500/10 bg-gradient-to-br from-dark-900/50 to-transparent">
            <p className="text-dark-200 text-xl leading-relaxed text-center italic">
              "At Shorubenix Info Technology, we don't just build projects — we build confidence, careers, and digital success."
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-12 items-center mb-20">
            <motion.div {...fadeInUp}>
              <h2 className="text-3xl font-display font-bold text-white mb-6">Our Approach</h2>
              <p className="text-dark-300 leading-relaxed mb-6">
                Our approach combines creativity, technical expertise, and practical implementation to ensure every client receives reliable and affordable solutions tailored to their needs.
              </p>
              <div className="space-y-4">
                {['Creativity & Design', 'Technical Expertise', 'Practical Implementation', 'Affordable Solutions'].map((item) => (
                  <div key={item} className="flex items-center gap-3">
                    <div className="w-1.5 h-1.5 rounded-full bg-primary-500" />
                    <span className="text-dark-200">{item}</span>
                  </div>
                ))}
              </div>
            </motion.div>
            <motion.div {...fadeInUp} className="grid grid-cols-2 gap-4">
              <div className="glass-card p-6 border-white/5 bg-primary-500/5">
                <Globe className="w-8 h-8 text-primary-400 mb-4" />
                <h3 className="text-xl font-display font-bold text-white mb-3">Our Mission</h3>
                <p className="text-dark-400 text-sm leading-relaxed">
                  To empower students, startups, and businesses with innovative, real-world IT solutions that create growth and opportunity.
                </p>
              </div>
              <div className="glass-card p-6 border-white/5 bg-accent-500/5 mt-8">
                <Target className="w-8 h-8 text-accent-400 mb-4" />
                <h3 className="text-xl font-display font-bold text-white mb-3">Our Vision</h3>
                <p className="text-dark-400 text-sm leading-relaxed">
                  To become a trusted and leading technology partner known for quality, innovation, and excellence.
                </p>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Timeline */}
      <section className="section-padding bg-dark-900/30">
        <div className="container-custom">
          <motion.div {...fadeInUp} className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-display font-bold mb-4">
              Our <span className="gradient-text">Journey</span>
            </h2>
          </motion.div>
          <div className="relative max-w-3xl mx-auto">
            <div className="absolute left-4 md:left-1/2 top-0 bottom-0 w-px bg-gradient-to-b from-primary-500/50 via-accent-500/50 to-transparent" />
            {timeline.map((item, i) => (
              <motion.div
                key={item.year}
                {...fadeInUp}
                transition={{ delay: i * 0.1 }}
                className={`relative flex items-start gap-8 mb-12 ${i % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse'}`}
              >
                <div className={`hidden md:block w-1/2 ${i % 2 === 0 ? 'text-right pr-8' : 'text-left pl-8'}`}>
                  <div className="glass-card p-6 inline-block">
                    <span className="text-sm font-display font-bold text-primary-400">{item.year}</span>
                    <h4 className="text-lg font-display font-semibold text-white mt-1">{item.title}</h4>
                    <p className="text-dark-400 text-sm mt-2">{item.desc}</p>
                  </div>
                </div>
                <div className="absolute left-4 md:left-1/2 w-3 h-3 rounded-full bg-primary-500 -translate-x-1.5 mt-2 ring-4 ring-dark-950" />
                <div className="md:hidden ml-12 glass-card p-6">
                  <span className="text-sm font-display font-bold text-primary-400">{item.year}</span>
                  <h4 className="text-lg font-display font-semibold text-white mt-1">{item.title}</h4>
                  <p className="text-dark-400 text-sm mt-2">{item.desc}</p>
                </div>
                <div className="hidden md:block w-1/2" />
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
