import StarBurst from "@/components/react-bits/star-burst";
import "./App.css";

function App() {
  return (
    <main className="site-shell">
      <StarBurst
        className="star-burst"
        color="#b3eab4"
        centerX={0.5}
        centerY={0.42}
        density={0.7}
        starCount={140}
        starSize={0.36}
        brightness={1.25}
        opacity={0.9}
        flowerIntensity={0.8}
      />

      <section className="hero-section" aria-label="Ciru AI">
        <div className="brand-mark">
          <img
            src="/ciruai.png"
            alt="Ciru AI"
            onError={(event) => {
              event.currentTarget.style.display = "none";
            }}
          />
        </div>
      </section>
    </main>
  );
}

export default App;
