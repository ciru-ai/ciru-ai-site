import { useEffect, useState } from "react";
import {
  ArrowDown,
  ArrowUpRight,
  GitBranch,
  HeartHandshake,
  Mail,
} from "lucide-react";
import StaggeredText from "@/components/react-bits/staggered-text";
import "./App.css";

const practices = [
  {
    number: "01",
    title: "Build local LLM systems",
    body: "Local LLM buildouts spanning model selection, adaptation, low-bit formats, and inference stacks shaped around the hardware and workload.",
  },
  {
    number: "02",
    title: "Measure what matters",
    body: "Task quality, tool use, memory, latency, throughput, and long-context behavior—published with enough context to challenge the result.",
  },
  {
    number: "03",
    title: "Engineer agents and workflows",
    body: "Agentic engineering and automated business workflows that connect models to tools, data, and clear human checkpoints.",
  },
];

const selectedWork = [
  {
    number: "01",
    title: "Ciru Inference Lab",
    body: "Measured local-model performance, quality, memory, and serving behavior—with the workload and context kept visible.",
    href: "https://llm.ciru.ai/",
    label: "Explore the lab",
  },
  {
    number: "02",
    title: "Invoice Sandbox",
    body: "A reproducible agent benchmark: 112 synthetic invoices, accounting traps, aggregation, and a useful final dashboard.",
    href: "https://llm.ciru.ai/invoicesandbox/",
    label: "See the benchmark",
  },
  {
    number: "03",
    title: "Open model releases",
    body: "Low-bit, accelerator-aware model artifacts with practical run notes and measured results on Hugging Face.",
    href: "https://huggingface.co/jcbtc",
    label: "Browse the models",
  },
];

const resources = [
  {
    title: "Live Benchmark Lab",
    note: "Current and completed evaluations",
    href: "https://lab.ciru.ai/",
  },
  {
    title: "Research Notes",
    note: "Reports, experiments, and findings",
    href: "https://llm.ciru.ai/research/",
  },
  {
    title: "Hugging Face",
    note: "Models and downloadable artifacts",
    href: "https://huggingface.co/jcbtc",
  },
  {
    title: "GitHub",
    note: "Code, fixtures, and open tooling",
    href: "https://github.com/ciru-ai",
  },
];

function usePrefersReducedMotion() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(() =>
    window.matchMedia("(prefers-reduced-motion: reduce)").matches,
  );

  useEffect(() => {
    const media = window.matchMedia("(prefers-reduced-motion: reduce)");
    const updatePreference = () => setPrefersReducedMotion(media.matches);

    media.addEventListener("change", updatePreference);
    return () => media.removeEventListener("change", updatePreference);
  }, []);

  return prefersReducedMotion;
}

function useDeferredHeroVideo(prefersReducedMotion: boolean) {
  const [shouldLoadVideo, setShouldLoadVideo] = useState(false);
  const saveData = Boolean(
    (navigator as Navigator & { connection?: { saveData?: boolean } })
      .connection?.saveData,
  );

  useEffect(() => {
    if (prefersReducedMotion || saveData) {
      return;
    }

    const timeoutId = window.setTimeout(() => setShouldLoadVideo(true), 700);
    return () => window.clearTimeout(timeoutId);
  }, [prefersReducedMotion, saveData]);

  return shouldLoadVideo && !prefersReducedMotion && !saveData;
}

function ExternalLink({
  href,
  children,
  className,
}: {
  href: string;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <a
      className={className}
      href={href}
      target="_blank"
      rel="noreferrer"
    >
      {children}
    </a>
  );
}

function App() {
  const prefersReducedMotion = usePrefersReducedMotion();
  const shouldLoadHeroVideo = useDeferredHeroVideo(prefersReducedMotion);
  const [heroVideoReady, setHeroVideoReady] = useState(false);

  return (
    <div className="site-shell">
      <header className="site-header">
        <a className="wordmark" href="#top" aria-label="Ciru.ai home">
          <span className="wordmark-mark" aria-hidden="true">
            C
          </span>
          <span>ciru.ai</span>
          <span className="wordmark-detail">research</span>
        </a>

        <nav className="desktop-nav" aria-label="Primary navigation">
          <a href="#practice">Practice</a>
          <a href="#work">Selected work</a>
          <a href="#resources">Resources</a>
          <a href="#support">Support</a>
        </nav>

        <a className="header-contact" href="mailto:jc@ciru.ai">
          <Mail size={15} aria-hidden="true" />
          <span>jc@ciru.ai</span>
        </a>
      </header>

      <main>
        <section className="hero" id="top" aria-labelledby="hero-title">
          <img
            className="hero-image-fallback"
            src="/assets/home/ciru-research-hero.webp"
            alt=""
            aria-hidden="true"
          />
          {shouldLoadHeroVideo && (
            <video
              className={`hero-video${heroVideoReady ? " is-ready" : ""}`}
              autoPlay
              muted
              loop
              playsInline
              preload="metadata"
              poster="/assets/home/ciru-research-hero.webp"
              disablePictureInPicture
              aria-hidden="true"
              onCanPlay={() => setHeroVideoReady(true)}
              onError={() => setHeroVideoReady(false)}
            >
              <source
                src="/assets/home/ciru-research-hero-loop-v2.mp4"
                type="video/mp4"
              />
            </video>
          )}
          <div className="hero-wash" aria-hidden="true" />

          <div className="hero-content">
            <div className="hero-kicker">
              <span>Independent AI Research</span>
            </div>

            <StaggeredText
              as="h1"
              className="hero-title"
              text={"Making advanced AI\nuseful, measurable,\nand local."}
              segmentBy="words"
              delay={54}
              duration={0.7}
              direction="bottom"
              blur
            />

            <p className="hero-copy">
              I research efficient inference, low-bit models, agent behavior,
              and rigorous evaluation—then turn that work into local LLM
              buildouts, agentic engineering, and automated workflows for
              businesses. Ciru is where the work becomes published models,
              reproducible benchmarks, and systems people can use.
            </p>

            <div className="hero-actions">
              <ExternalLink
                className="button button-primary"
                href="https://llm.ciru.ai/"
              >
                Explore the lab
                <ArrowUpRight size={17} aria-hidden="true" />
              </ExternalLink>
              <a className="button button-secondary" href="mailto:jc@ciru.ai">
                Email me
                <Mail size={16} aria-hidden="true" />
              </a>
            </div>

            <div className="focus-line" aria-label="Research focus">
              <span>Efficient inference</span>
              <span>Local LLM buildouts</span>
              <span>Agentic engineering</span>
              <span>Workflow automation</span>
              <span>Reproducible evaluation</span>
            </div>
          </div>

          <a className="scroll-cue" href="#practice">
            <span>Continue</span>
            <ArrowDown size={15} aria-hidden="true" />
          </a>
        </section>

        <section className="section practice-section" id="practice">
          <div className="section-heading">
            <p className="section-kicker">The practice</p>
            <h2>Research should survive contact with reality.</h2>
            <p>
              Ciru works across the whole path—from models and local
              infrastructure to agents, workflows, and a result someone else
              can examine.
            </p>
          </div>

          <div className="practice-grid">
            {practices.map((practice) => (
              <article className="practice-card" key={practice.number}>
                <span className="card-number">{practice.number}</span>
                <h3>{practice.title}</h3>
                <p>{practice.body}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="section work-section" id="work">
          <div className="work-stage">
            <img
              className="work-stage-image"
              src="/assets/home/ciru-evaluation-bench.webp"
              alt="Abstract research instrument representing model evaluation and deployment"
            />
            <div className="work-stage-wash" aria-hidden="true" />

            <div className="work-panel">
              <div className="work-intro">
                <p className="section-kicker">Selected systems</p>
                <h2>Work you can inspect.</h2>
                <p>
                  The interesting part is not the claim. It is the artifact, the
                  method, and what happened when it ran.
                </p>
              </div>

              <div className="work-list">
                {selectedWork.map((item) => (
                  <ExternalLink
                    className="work-item"
                    href={item.href}
                    key={item.number}
                  >
                    <span className="card-number">{item.number}</span>
                    <span className="work-item-copy">
                      <strong>{item.title}</strong>
                      <span>{item.body}</span>
                      <small>
                        {item.label}
                        <ArrowUpRight size={14} aria-hidden="true" />
                      </small>
                    </span>
                  </ExternalLink>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section className="section resources-section" id="resources">
          <div className="resources-copy">
            <p className="section-kicker">Open doors</p>
            <h2>Follow the evidence.</h2>
            <p>
              Benchmarks, research notes, model artifacts, and source code are
              public wherever they can be.
            </p>
          </div>

          <div className="resource-list">
            {resources.map((resource, index) => (
              <ExternalLink
                className="resource-item"
                href={resource.href}
                key={resource.title}
              >
                <span className="resource-index">0{index + 1}</span>
                <span className="resource-name">
                  <strong>{resource.title}</strong>
                  <small>{resource.note}</small>
                </span>
                {resource.title === "GitHub" ? (
                  <GitBranch size={19} aria-hidden="true" />
                ) : (
                  <ArrowUpRight size={19} aria-hidden="true" />
                )}
              </ExternalLink>
            ))}
          </div>
        </section>

        <section
          className="section support-section"
          id="support"
          aria-labelledby="support-title"
        >
          <div className="support-card">
            <div className="support-copy">
              <p className="section-kicker">Keep the lab moving</p>
              <h2 id="support-title">Support independent Ciru research.</h2>
              <p>
                If the models, benchmarks, and open technical work are useful
                to you, you can make a one-time payment in any amount you
                choose. Support helps fund compute, evaluation, and continued
                publication of the work.
              </p>
            </div>

            <div className="support-action">
              <ExternalLink
                className="button button-primary support-button"
                href="https://buy.stripe.com/aFa14n6ZfbQpfql5T8bMQ00"
              >
                Choose your amount
                <HeartHandshake size={18} aria-hidden="true" />
              </ExternalLink>
              <p className="support-note">
                This is voluntary, one-time support. It does not purchase
                consulting services, create a subscription, or promise a
                deliverable. Ciru does not represent it as a tax-deductible
                charitable contribution.
              </p>
              <p className="support-contact">
                Made a payment in error or need help? Email{" "}
                <a href="mailto:jc@ciru.ai">jc@ciru.ai</a> with the receipt
                email so the payment can be reviewed.
              </p>
            </div>
          </div>
        </section>

        <section className="contact-section" aria-labelledby="contact-title">
          <div className="contact-orbit" aria-hidden="true" />
          <div className="contact-icon" aria-hidden="true">
            <GitBranch size={22} />
          </div>
          <p className="section-kicker">Ways to work with Ciru</p>
          <h2 id="contact-title">
            Strengthen the commons. Build what your organization needs.
          </h2>
          <p className="contact-intro">
            Ciru works in public where research can strengthen the ecosystem,
            and commercially where organizations need focused engineering.
          </p>

          <div className="engagement-grid">
            <article className="engagement-card">
              <span className="engagement-label">Open source</span>
              <h3>Give back upstream.</h3>
              <p>
                Ciru returns research to the ecosystem through reproducible
                evidence, practical build notes, open artifacts, and focused
                upstream contributions.
              </p>
              <a
                className="engagement-link engagement-link-secondary"
                href="mailto:jc@ciru.ai?subject=Open%20source%20conversation"
              >
                Connect on open source
                <ArrowUpRight size={17} aria-hidden="true" />
              </a>
            </article>

            <article className="engagement-card engagement-card-services">
              <span className="engagement-label">Professional services</span>
              <h3>Turn advanced AI into working systems.</h3>
              <p>
                Ciru works with organizations on local LLM systems, agentic
                engineering, rigorous evaluation, and workflow automation
                through separately scoped commercial engagements.
              </p>
              <a
                className="engagement-link engagement-link-primary"
                href="mailto:jc@ciru.ai?subject=Ciru%20project%20inquiry"
              >
                Discuss a project
                <ArrowUpRight size={17} aria-hidden="true" />
              </a>
            </article>
          </div>
        </section>
      </main>

      <footer className="site-footer">
        <div>
          <span className="footer-brand">ciru.ai</span>
          <span>AI research &amp; engineering</span>
        </div>
        <div>
          <span>Crown Citadel Group LLC</span>
          <span>© 2026</span>
        </div>
      </footer>
    </div>
  );
}

export default App;
