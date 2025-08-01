'use client'
import Image from "next/image";
import { useState } from "react";
type AnalyzeResult = {
  total_comments: number;
  positive_score: number;
  summary: string;
  suggestions: string;
};

export default function Home() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState<AnalyzeResult | null>(null);
  const [loading, setLoading] = useState(false);

  const analyzeVideo = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ youtube_url: url })
      });

      if (!response.ok) throw new Error("Failed to analyze video");

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error:", error);
      alert("Something went wrong!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-100 w-full flex flex-col items-center justify-center">
      <div className="min-h-screen max-w-7xl px-4 sm:px-6 lg:px-8 grid md:grid-cols-5 gap-4 py-12">
        <div className="md:col-span-2 flex flex-col items-center justify-center w-full">
          <div className="bg-white/80 backdrop-blur-xl rounded-[22px] p-8 rounded-3xl border-gradient-to-tr from-indigo-400 via-blue-400 to-purple-400 shadow-xl animate-border-glow">
            <div className="flex flex-col items-center mb-6">
              <span className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-tr from-indigo-500 to-blue-400 shadow-lg mb-2">
                <Image src="/favicon.png" alt="YouTube Icon" width={32} height={32} className="w-8 h-8" />
              </span>
              <h1 className="text-3xl font-extrabold text-indigo-700 mb-1 py-3 text-center tracking-tight drop-shadow">YouTube Comment Analyzer</h1>
              <p className="text-gray-500 text-center">Get instant insights and suggestions for your YouTube videos!</p>
            </div>
            <div className="mb-6 relative">
              <input
                type="text"
                id="youtube-url"
                placeholder=""
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="peer w-full px-4 py-3 text-gray-400 rounded-lg border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all duration-200 bg-white shadow-sm placeholder-transparent"
                disabled={loading}
                autoComplete="off"
              />
              <label
                htmlFor="youtube-url"
                className="absolute left-4 top-3 text-gray-400 text-base transition-all duration-200 pointer-events-none peer-placeholder-shown:top-3 peer-placeholder-shown:text-base peer-focus:-top-3 peer-focus:text-xs peer-focus:text-indigo-600 bg-white px-1 peer-[&:not(:placeholder-shown)]:-top-3 peer-[&:not(:placeholder-shown)]:text-xs peer-[&:not(:placeholder-shown)]:text-indigo-600"
              >
                Paste YouTube video URL
              </label>
            </div>
            <button
              onClick={analyzeVideo}
              className={`w-full py-3 rounded-lg font-semibold text-white bg-gradient-to-r from-indigo-500 to-blue-500 shadow-lg hover:scale-105 hover:from-indigo-600 hover:to-blue-600 transition-all duration-200 active:scale-95 flex items-center justify-center gap-2 ${
                loading ? "opacity-60 cursor-not-allowed" : ""
              }`}
              disabled={loading}
            >
              {loading ? (
                <>
                  <svg className="animate-spin h-5 w-5 mr-2 text-white" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
                  </svg>
                  Analyzing...
                </>
              ) : (
                "Analyze"
              )}
            </button>
          </div>
        </div>
        <div className="mt-10 animate-fade-in md:col-span-3 flex flex-col items-stretch justify-start w-full pl-3">
          {result ? (<div className="p-8">
            <h2 className="text-xl font-bold text-indigo-600 mb-4 text-center flex items-center justify-center gap-2">
              <svg className="w-6 h-6 text-indigo-500" fill="none" stroke="currentColor" strokeWidth={2.2} viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9 9 4.03 9 9z" />
              </svg>
              Results
            </h2>
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-4">
                <div className="flex flex-col items-center gap-3 bg-indigo-50 rounded-lg px-4 py-2">
                  <span className="text-indigo-600 font-medium pt-1 flex-1">Total Comments</span>
                  <span className="font-bold text-3xl py-3 text-indigo-800">{result.total_comments}</span>
                </div>
                <div className="flex flex-col items-center gap-3 bg-blue-50 rounded-lg px-4 py-2">
                  <span className="text-blue-600 font-medium pt-1 flex-1">Positive Score</span>
                  <span className="font-bold text-3xl py-3 text-blue-800">{result.positive_score}%</span>
                </div>
              </div>
              <div className="space-y-2 max-h-48 overflow-y-auto pr-2 gap-4">
                <div className="bg-purple-50 rounded-lg px-4 py-2">
                  <span className="text-purple-600 font-medium">Summary</span>
                  <p className="text-gray-800 mt-1">{result.summary}</p>
                </div>
                <div className="bg-green-50 rounded-lg px-4 py-2">
                  <span className="text-green-600 font-medium">Suggestions</span>
                  <p className="text-gray-800 mt-1">{result.suggestions}</p>
                </div>
              </div>
            </div>
          </div>
          ): <div className="text-center space-y-6 p-10 m-3 animate-fade-in">
            <h2 className="text-2xl font-bold text-indigo-600 flex items-center justify-center gap-2">
              <Image src="/favicon.png" alt="YouTube Icon" width={32} height={32} className="w-8 h-8 mr-5" />
              Welcome to YouTube Comment Analyzer
            </h2>
            <p className="text-gray-600 text-base px-5 pb-3">
              Analyze any YouTube video in seconds! Get total comment count, positive feedback score, a concise summary, 
              and AI‑powered suggestions to improve your content.
            </p>
            <div className="space-y-4 text-left">
              <h3 className="text-lg font-semibold text-indigo-700">How to Use:</h3>
              <p className="text-gray-600">Follow these simple steps to get started:</p>
              <div className="flex items-start gap-3 ml-3">
                <span className="flex-shrink-0 w-6 h-6 bg-indigo-500 text-white rounded-full flex items-center justify-center text-sm font-bold">1</span>
                <p className="text-gray-700">Paste your <span className="font-semibold">YouTube video URL</span> in the input field above.</p>
              </div>
              <div className="flex items-start gap-3 ml-3">
                <span className="flex-shrink-0 w-6 h-6 bg-indigo-500 text-white rounded-full flex items-center justify-center text-sm font-bold">2</span>
                <p className="text-gray-700">Click the <span className="font-semibold">Analyze</span> button to process the video in real time.</p>
              </div>
              <div className="flex items-start gap-3 ml-3">
                <span className="flex-shrink-0 w-6 h-6 bg-indigo-500 text-white rounded-full flex items-center justify-center text-sm font-bold">3</span>
                <p className="text-gray-700">View results including <span className="font-semibold">Total Comments, Positive Score, Summary</span>, and 
                  <span className="font-semibold"> AI Suggestions</span> for your content.</p>
              </div>
            </div>
            <div className="mt-10 flex justify-center">
              <div className="px-5 py-3 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-full text-sm shadow-md animate-pulse">
                Enter a YouTube link to get started!
              </div>
            </div>
          </div>}
        </div>
      </div>
      <style jsx global>{`
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(16px);}
          to { opacity: 1; transform: translateY(0);}
        }
        .animate-fade-in {
          animation: fade-in 0.7s cubic-bezier(.4,0,.2,1) both;
        }
        @keyframes border-glow {
          0%, 100% { box-shadow: 0 0 24px 4px #6366f1, 0 0 0 0 #3b82f6; }
          50% { box-shadow: 0 0 32px 8px #3b82f6, 0 0 0 0 #6366f1; }
        }
        .animate-border-glow {
          animation: border-glow 2.5s infinite alternate;
        }
      `}</style>
    </main>
  );
}