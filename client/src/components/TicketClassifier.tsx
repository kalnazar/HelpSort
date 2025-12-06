import { useState, useEffect, useRef } from "react";
import TicketResults from "./TicketResults";

interface BackendResult {
  topic: string;
  topic_id: number;
  priority: string;
  priority_id: number;
  routing: string;
  routing_id: number;
}

interface ClassificationResult {
  category: string;
  assignee: string;
  priority: string;
  description: string;
}

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000";

export default function TicketClassifier() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<ClassificationResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [visibleSuggestions, setVisibleSuggestions] = useState<string[]>([]);
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const isMobile = window.innerWidth < 640; // <640px → Tailwind "sm"
  const SLOTS = isMobile ? 2 : 4;

  const suggestions: string[] = [
    "Payment failed after submitting card details",
    "Can't log into my account, password reset not working",
    "Mobile app crashes when uploading attachments",
    "Order shows as paid but not delivered",
    "Unable to integrate API - 401 unauthorized error",
    "Feature request: export reports in CSV",
    "Delay in email notifications from system",
    "Incorrect billing amount on invoice",
    "Request to change account subscription plan",
    "Data sync error between services overnight",
    "Refund not processed after approval",
    "Two-factor authentication codes not received",
  ];

  const classifyTicket = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch(`${API_BASE_URL}/classify`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error || "Server error");
      }

      const data: BackendResult = await res.json();

      setResult({
        category: data.topic,
        assignee: data.routing,
        priority: data.priority,
        description: text,
      });
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Something went wrong while classifying.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const isMobile = window.innerWidth < 640;
    const SLOTS = isMobile ? 2 : 4;

    let poolIndex = 0;

    setVisibleSuggestions(
      Array.from(
        { length: SLOTS },
        (_, i) => suggestions[(poolIndex + i) % suggestions.length]
      )
    );
    poolIndex = (poolIndex + SLOTS) % suggestions.length;

    const interval = setInterval(() => {
      setVisibleSuggestions((prev) => {
        if (prev.length === 0) return prev;
        const next = [...prev];
        next.shift();
        next.push(suggestions[poolIndex]);
        poolIndex = (poolIndex + 1) % suggestions.length;
        return next;
      });
    }, 4000);

    return () => clearInterval(interval);
  }, []);

  const applySuggestion = (s: string) => {
    setText(s);
    requestAnimationFrame(() => {
      const el = textareaRef.current;
      if (el) {
        el.focus();
        el.selectionStart = el.selectionEnd = el.value.length;
      }
    });
  };

  return (
    <div className="relative z-10 max-w-4xl mx-auto px-4 py-12">
      <div className="space-y-8">
        {/* Input Section */}
        <div className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-2xl p-8 hover:border-white/20 transition-colors">
          <form onSubmit={classifyTicket} className="space-y-6">
            <div>
              <label className="block text-sm font-semibold text-white/90 mb-3">
                Describe your support ticket
              </label>
              <textarea
                ref={textareaRef}
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="e.g., I'm experiencing a critical bug when trying to process payments through the API..."
                className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder:text-white/40 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/20 transition-all resize-none"
                rows={5}
              />
              {/* Suggestions */}
              <div className="mt-4 suggestions">
                {visibleSuggestions.map((s, idx) => (
                  <button
                    key={`${s}-${idx}`}
                    type="button"
                    className="chip"
                    onClick={() => applySuggestion(s)}
                    aria-label={`Use suggestion ${idx + 1}`}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>

            <button
              type="submit"
              disabled={!text.trim() || isLoading}
              className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-bold py-3 rounded-xl transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? "Classifying..." : "Classify Ticket"}
            </button>
          </form>

          {error && <p className="mt-4 text-sm text-red-400">{error}</p>}
        </div>

        {/* Results Section */}
        {result && <TicketResults result={result} />}
      </div>
    </div>
  );
}
