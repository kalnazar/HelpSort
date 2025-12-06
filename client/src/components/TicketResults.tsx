import { useState, useEffect } from "react";

interface ClassificationResult {
  category: string;
  assignee: string;
  priority: string;
  description: string;
}

interface TicketResultsProps {
  result: ClassificationResult;
}

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000";

export default function TicketResults({ result }: TicketResultsProps) {
  const [labels, setLabels] = useState<string[]>([]);
  const [labelsLoading, setLabelsLoading] = useState(true);

  useEffect(() => {
    const fetchLabels = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/labels`);
        if (res.ok) {
          const data = await res.json();
          setLabels(data.routing_labels || []);
        }
      } catch (err) {
        console.error("Error fetching labels:", err);
      } finally {
        setLabelsLoading(false);
      }
    };
    fetchLabels();
  }, []);
  const getPriorityBadgeColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case "critical":
        return "bg-red-500/20 text-red-400 border-red-500/30";
      case "high":
        return "bg-orange-500/20 text-orange-400 border-orange-500/30";
      case "medium":
        return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30";
      default:
        return "bg-green-500/20 text-green-400 border-green-500/30";
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-2xl p-8">
        <div className="space-y-6">
          <div className="space-y-2">
            <h3 className="text-xs uppercase tracking-widest text-white/60 font-semibold">
              Classification Result
            </h3>
            <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              {result.category}
            </h2>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3">
            <div className="space-y-2">
              <p className="text-xs text-white/60 uppercase tracking-widest font-semibold">
                Priority
              </p>
              <span
                className={`inline-flex items-center px-3 py-1 rounded-lg text-sm font-semibold border ${getPriorityBadgeColor(
                  result.priority
                )}`}
              >
                {result.priority}
              </span>
            </div>

            <div className="space-y-2 sm:col-span-1 md:col-span-2">
              <p className="text-xs text-white/60 uppercase tracking-widest font-semibold">
                Assigned To
              </p>
              <p className="text-white font-semibold">{result.assignee}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Possible assignees list (from backend) */}
      <div className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-2xl p-8">
        <div className="space-y-4">
          <h3 className="text-sm font-semibold text-white/90">
            Possible Assignees
          </h3>
          <p className="text-xs text-white/60">
            Support queues where tickets may be routed:
          </p>
          <div className="flex flex-wrap gap-2 mt-2">
            {labelsLoading ? (
              <p className="text-xs text-white/60">Loading labels...</p>
            ) : labels.length > 0 ? (
              labels.map((team) => {
                const isPredicted =
                  team.toLowerCase() === result.assignee.toLowerCase();
                return (
                  <span
                    key={team}
                    className={`px-3 py-1 rounded-full text-sm font-medium border ${
                      isPredicted
                        ? "bg-blue-600 text-white border-blue-500"
                        : "bg-white/5 text-white/80 border-white/10"
                    }`}
                  >
                    {team}
                  </span>
                );
              })
            ) : (
              <p className="text-xs text-white/60">No labels available.</p>
            )}
          </div>
          <p className="text-xs text-white/60 mt-2">
            The highlighted item shows the model's predicted routing.
          </p>
        </div>
      </div>

      {/* Ticket Details */}
      <div className="backdrop-blur-sm bg-white/5 border border-white/10 rounded-2xl p-8">
        <div className="space-y-4">
          <h3 className="text-sm font-semibold text-white/90">
            Ticket Content
          </h3>
          <div className="bg-white/5 border border-white/5 rounded-lg p-4 text-white/80 text-sm leading-relaxed whitespace-pre-wrap break-words">
            {result.description}
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <button
          onClick={() =>
            navigator.clipboard.writeText(JSON.stringify(result, null, 2))
          }
          className="px-6 py-3 bg-white/10 hover:bg-white/20 border border-white/20 rounded-lg text-white font-medium transition-colors"
        >
          Copy Result
        </button>
        <button
          onClick={() => window.location.reload()}
          className="px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 rounded-lg text-white font-semibold transition-all"
        >
          Classify Another
        </button>
      </div>
    </div>
  );
}
