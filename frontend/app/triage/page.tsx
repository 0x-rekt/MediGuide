"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { triageSymptoms } from "@/lib/api";

const LANGUAGES = [
  { code: "en", name: "English" },
  { code: "ja", name: "Japanese" },
  { code: "th", name: "Thai" },
  { code: "zh", name: "Chinese" },
  { code: "ko", name: "Korean" },
  { code: "fr", name: "French" },
  { code: "de", name: "German" },
  { code: "es", name: "Spanish" },
  { code: "ar", name: "Arabic" },
  { code: "hi", name: "Hindi" },
];

const QUICK_SYMPTOMS = [
  "Fever and chills",
  "Chest pain",
  "Severe headache",
  "Difficulty breathing",
  "Stomach pain",
  "Broken bone / injury",
];

export default function TriagePage() {
  const router = useRouter();
  const [symptoms, setSymptoms] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("");
  const [language, setLanguage] = useState("en");
  const [location, setLocation] = useState<{ lat: number; lng: number } | null>(
    null,
  );
  const [locStatus, setLocStatus] = useState<
    "idle" | "loading" | "got" | "error"
  >("idle");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);

  const getLocation = () => {
    setLocStatus("loading");
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setLocation({ lat: pos.coords.latitude, lng: pos.coords.longitude });
        setLocStatus("got");
      },
      () => setLocStatus("error"),
      { timeout: 8000 },
    );
  };

  const handleSubmit = async () => {
    if (!symptoms.trim()) {
      setError("Please describe your symptoms.");
      return;
    }
    if (!location) {
      setError("Location is required to find nearby hospitals.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const result = await triageSymptoms({
        symptoms,
        latitude: location.lat,
        longitude: location.lng,
        language,
        radius_meters: 15000,
        age: age ? parseInt(age) : undefined,
        gender: gender || undefined,
      });
      sessionStorage.setItem("triageResult", JSON.stringify(result));
      router.push("/results");
    } catch (e: unknown) {
      setError(
        e instanceof Error
          ? e.message
          : "Something went wrong. Please try again.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "calc(100vh - 64px)",
        background: "var(--background)",
        padding: "3rem 1.5rem",
      }}
    >
      <div style={{ maxWidth: "680px", margin: "0 auto" }}>
        {/* Header */}
        <div
          className={mounted ? "fade-up" : ""}
          style={{ marginBottom: "2.5rem" }}
        >
          <p
            style={{
              fontSize: "0.75rem",
              letterSpacing: "0.15em",
              color: "var(--primary)",
              textTransform: "uppercase",
              marginBottom: "0.75rem",
            }}
          >
            STEP 1 OF 3 · SYMPTOM ASSESSMENT
          </p>
          <h1
            style={{
              fontFamily: "var(--font-bebas)",
              fontSize: "clamp(2.5rem, 6vw, 4rem)",
              letterSpacing: "0.03em",
              color: "var(--foreground)",
              lineHeight: 1,
              marginBottom: "0.75rem",
            }}
          >
            WHAT ARE YOU FEELING?
          </h1>
          <p style={{ color: "var(--foreground-dim)", fontSize: "1rem" }}>
            Be as specific as possible — duration, intensity, and location of
            symptoms all help.
          </p>
        </div>

        {/* Quick select */}
        <div
          className={mounted ? "fade-up-delay-1" : ""}
          style={{ marginBottom: "1.5rem" }}
        >
          <span className="label">Quick select</span>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
            {QUICK_SYMPTOMS.map((s) => (
              <button
                key={s}
                onClick={() =>
                  setSymptoms((prev) => (prev ? `${prev}, ${s}` : s))
                }
                style={{
                  background: symptoms.includes(s)
                    ? "rgba(0,212,168,0.1)"
                    : "var(--surface)",
                  border: `1px solid ${symptoms.includes(s) ? "rgba(0,212,168,0.3)" : "var(--border)"}`,
                  color: symptoms.includes(s)
                    ? "var(--primary)"
                    : "var(--foreground-dim)",
                  borderRadius: "100px",
                  padding: "0.4rem 1rem",
                  fontSize: "0.85rem",
                  cursor: "pointer",
                  transition: "all 0.2s",
                }}
              >
                {s}
              </button>
            ))}
          </div>
        </div>

        {/* Symptom textarea */}
        <div
          className={`card ${mounted ? "fade-up-delay-1" : ""}`}
          style={{ padding: "1.5rem", marginBottom: "1.5rem" }}
        >
          <span className="label">Describe your symptoms *</span>
          <textarea
            className="input-field"
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            placeholder="e.g. I have a severe headache and fever since yesterday, along with neck stiffness and sensitivity to light..."
            rows={5}
            style={{ resize: "vertical", lineHeight: 1.6 }}
          />
          <div
            style={{
              display: "flex",
              justifyContent: "flex-end",
              marginTop: "0.5rem",
            }}
          >
            <span
              style={{
                fontSize: "0.75rem",
                color:
                  symptoms.length > 20
                    ? "var(--primary)"
                    : "var(--foreground-muted)",
              }}
            >
              {symptoms.length} chars{" "}
              {symptoms.length < 20 && symptoms.length > 0
                ? "— add more detail"
                : ""}
            </span>
          </div>
        </div>

        {/* Patient info */}
        <div
          className={`card ${mounted ? "fade-up-delay-2" : ""}`}
          style={{ padding: "1.5rem", marginBottom: "1.5rem" }}
        >
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "1rem",
              marginBottom: "1rem",
            }}
          >
            <div>
              <span className="label">Age (optional)</span>
              <input
                type="number"
                className="input-field"
                placeholder="e.g. 34"
                value={age}
                onChange={(e) => setAge(e.target.value)}
                min={1}
                max={120}
              />
            </div>
            <div>
              <span className="label">Gender (optional)</span>
              <select
                className="input-field"
                value={gender}
                onChange={(e) => setGender(e.target.value)}
                style={{ appearance: "none", cursor: "pointer" }}
              >
                <option value="">Select</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
            </div>
          </div>
          <div>
            <span className="label">Your language</span>
            <select
              className="input-field"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              style={{ appearance: "none", cursor: "pointer" }}
            >
              {LANGUAGES.map((l) => (
                <option key={l.code} value={l.code}>
                  {l.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Location */}
        <div
          className={`card ${mounted ? "fade-up-delay-3" : ""}`}
          style={{ padding: "1.5rem", marginBottom: "1.5rem" }}
        >
          <span className="label">Your location *</span>
          <p
            style={{
              color: "var(--foreground-dim)",
              fontSize: "0.9rem",
              marginBottom: "1rem",
            }}
          >
            Required to find hospitals near you.
          </p>
          <button
            onClick={getLocation}
            disabled={locStatus === "loading" || locStatus === "got"}
            className={locStatus === "got" ? "" : "btn-primary"}
            style={
              locStatus === "got"
                ? {
                    background: "rgba(34,197,94,0.1)",
                    border: "1px solid rgba(34,197,94,0.3)",
                    color: "#22c55e",
                    padding: "0.75rem 1.5rem",
                    borderRadius: "8px",
                    cursor: "default",
                    display: "flex",
                    alignItems: "center",
                    gap: "0.5rem",
                    fontWeight: 600,
                  }
                : { display: "flex", alignItems: "center", gap: "0.5rem" }
            }
          >
            {locStatus === "loading" && <div className="spinner" />}
            {locStatus === "got" && "✓"}
            {locStatus === "idle" && "📍"}
            {locStatus === "idle" && "Detect My Location"}
            {locStatus === "loading" && "Detecting..."}
            {locStatus === "got" &&
              `Location captured (${location?.lat.toFixed(3)}, ${location?.lng.toFixed(3)})`}
            {locStatus === "error" && "Retry Location"}
          </button>
          {locStatus === "error" && (
            <p
              style={{
                color: "var(--severity-high)",
                fontSize: "0.85rem",
                marginTop: "0.5rem",
              }}
            >
              Could not get location. Please enable location permissions and try
              again.
            </p>
          )}
        </div>

        {/* Error */}
        {error && (
          <div
            style={{
              background: "rgba(239,68,68,0.08)",
              border: "1px solid rgba(239,68,68,0.25)",
              borderRadius: "8px",
              padding: "0.875rem 1rem",
              color: "var(--severity-emergency)",
              fontSize: "0.9rem",
              marginBottom: "1.5rem",
            }}
          >
            ⚠ {error}
          </div>
        )}

        {/* Submit */}
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="btn-primary"
          style={{
            width: "100%",
            justifyContent: "center",
            fontSize: "1.05rem",
            padding: "1rem",
          }}
        >
          {loading ? (
            <>
              <div className="spinner" />
              Analyzing symptoms & finding hospitals...
            </>
          ) : (
            "Find Help Now →"
          )}
        </button>

        <p
          style={{
            textAlign: "center",
            color: "var(--foreground-muted)",
            fontSize: "0.8rem",
            marginTop: "1rem",
          }}
        >
          🔒 Your data is private and not shared with third parties
        </p>
      </div>
    </div>
  );
}
