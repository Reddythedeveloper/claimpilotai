"use client";

import { useState, useEffect, use } from "react";
import { motion } from "framer-motion";
import { Activity, ArrowLeft, RefreshCw, FileText, CheckCircle, AlertTriangle, Play } from "lucide-react";
import Link from "next/link";

interface WorkflowResult {
  status: string;
  evaluation?: {
    decision: string;
    confidence_score: number;
    reasoning: string;
  };
  evidence_count?: number;
  messages?: string[];
  error?: string;
}

interface CaseData {
  payer: string;
  amount: number;
  denial_reason: string;
  procedure_code: string;
  diagnosis_code: string;
  member_plan: string;
  notes: string;
}

export default function CaseDetail({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const caseId = resolvedParams.id;
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<WorkflowResult | null>(null);
  const [caseData, setCaseData] = useState<CaseData | null>(null);

  useEffect(() => {
    // Fetch case data
    fetch(`http://localhost:8000/cases/${caseId}`)
      .then(res => {
        if (!res.ok) throw new Error("Case not found");
        return res.json();
      })
      .then(data => {
        setCaseData(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });

    // Check if workflow is already running or completed
    fetch(`http://localhost:8000/workflows/${caseId}/summary`)
      .then(res => {
        if (res.ok) return res.json();
        return null;
      })
      .then(data => {
        if (data) {
          if (data.status === "running") {
            setRunning(true);
            startPolling();
          } else {
            setResult(data);
          }
        }
      })
      .catch(err => console.log("No previous workflow", err));
      
      // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [caseId]);

  const startPolling = () => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`http://localhost:8000/workflows/${caseId}/summary`);
        if (res.ok) {
          const data = await res.json();
          if (data.status === "completed" || data.status === "failed") {
            setResult(data);
            setRunning(false);
            clearInterval(interval);
          }
        }
      } catch (err) {
        console.error("Polling error", err);
      }
    }, 2000);
  };

  const handleRunWorkflow = async () => {
    setRunning(true);
    try {
      const res = await fetch(`http://localhost:8000/workflows/${caseId}/run`, {
        method: "POST"
      });
      if (!res.ok) throw new Error("Failed to trigger workflow");
      startPolling();
    } catch (err) {
      console.error(err);
      setRunning(false);
    }
  };

  if (loading) {
    return (
      <main className="min-h-screen p-8 md:p-16 max-w-7xl mx-auto flex justify-center items-center">
        <RefreshCw className="animate-spin text-blue-400" size={48} />
      </main>
    );
  }

  if (!caseData) {
    return (
      <main className="min-h-screen p-8 md:p-16 max-w-7xl mx-auto text-center">
        <h1 className="text-4xl font-bold text-white mb-4">Case Not Found</h1>
        <Link href="/" className="text-blue-400 hover:text-blue-300">Return to Dashboard</Link>
      </main>
    );
  }

  return (
    <main className="min-h-screen p-8 md:p-16 max-w-7xl mx-auto">
      <Link href="/" className="inline-flex items-center gap-2 text-blue-400 hover:text-blue-300 mb-8 transition-colors">
        <ArrowLeft size={20} /> Back to Dashboard
      </Link>
      
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between mb-8"
      >
        <div>
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
            Case: {caseId}
          </h1>
          <p className="text-gray-400 mt-2">Denied Claim Review</p>
        </div>
        
        <button 
          onClick={handleRunWorkflow}
          disabled={running || result !== null}
          className={`glass-button px-6 py-3 rounded-full font-semibold flex items-center gap-2
            ${(running || result !== null) ? 'opacity-50 cursor-not-allowed' : ''}
          `}
        >
          {running ? <RefreshCw className="animate-spin" size={20} /> : <Play size={20} />}
          {running ? 'Running Analysis...' : 'Run Agent Workflow'}
        </button>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="glass-panel p-8"
        >
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2 border-b border-white/10 pb-4">
            <FileText className="text-blue-400" /> Claim Details
          </h2>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-400">Payer</p>
                <p className="font-medium">{caseData.payer}</p>
              </div>
              <div>
                <p className="text-sm text-gray-400">Billed Amount</p>
                <p className="font-mono text-lg">${caseData.amount.toFixed(2)}</p>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-400">Procedure Code</p>
                <p className="font-mono">{caseData.procedure_code}</p>
              </div>
              <div>
                <p className="text-sm text-gray-400">Diagnosis</p>
                <p className="font-mono">{caseData.diagnosis_code}</p>
              </div>
            </div>
            
            <div className="bg-red-500/10 border border-red-500/20 p-4 rounded-lg mt-6">
              <p className="text-sm text-red-400 mb-1">Denial Reason</p>
              <p className="font-medium text-red-200">{caseData.denial_reason}</p>
            </div>
            
            <div className="bg-white/5 border border-white/10 p-4 rounded-lg">
              <p className="text-sm text-gray-400 mb-1">Provider Notes</p>
              <p className="font-medium text-gray-200">{caseData.notes}</p>
            </div>
          </div>
        </motion.div>

        {result && (
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="glass-panel p-8 flex flex-col"
          >
            <h2 className="text-xl font-semibold mb-6 flex items-center gap-2 border-b border-white/10 pb-4">
              <Activity className="text-purple-400" /> AI Recommendation
            </h2>
            
            {result.status === "failed" ? (
              <div className="text-red-400">Workflow Failed: {result.error}</div>
            ) : (
              <div className="flex-1 space-y-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-400 mb-1">Decision</p>
                    <div className="flex items-center gap-2">
                      <CheckCircle className={result.evaluation?.decision === 'Approved' ? 'text-green-400' : 'text-red-400'} size={24} />
                      <span className={`text-2xl font-bold ${result.evaluation?.decision === 'Approved' ? 'text-green-400' : 'text-red-400'}`}>
                        {result.evaluation?.decision}
                      </span>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-400 mb-1">Confidence</p>
                    <span className="text-2xl font-mono">{(result.evaluation?.confidence_score! * 100).toFixed(1)}%</span>
                  </div>
                </div>
                
                <div className="bg-blue-500/10 border border-blue-500/20 p-4 rounded-lg">
                  <p className="text-sm text-blue-400 mb-2">Agent Reasoning</p>
                  <p className="text-gray-200 leading-relaxed">{result.evaluation?.reasoning}</p>
                </div>
                
                <div>
                  <p className="text-sm text-gray-400 mb-3">Workflow Trace Logs</p>
                  <div className="space-y-2 font-mono text-xs max-h-48 overflow-y-auto">
                    {result.messages?.map((msg, i) => (
                      <div key={i} className="flex gap-2 text-gray-300">
                        <span className="text-purple-400 shrink-0">[{i+1}]</span> 
                        <span className="break-all">{msg}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </motion.div>
        )}
        
        {!result && (
          <div className="glass-panel p-8 flex flex-col items-center justify-center text-center border-dashed border-2 border-white/10 opacity-60">
            <Activity className="text-gray-500 mb-4" size={48} />
            <h3 className="text-xl font-semibold text-gray-400">
              {running ? "Analyzing Claim..." : "Awaiting Analysis"}
            </h3>
            <p className="text-sm text-gray-500 mt-2 max-w-sm">
              {running 
                ? "The multi-agent system is currently retrieving evidence and evaluating the claim."
                : "Run the multi-agent workflow to retrieve relevant policy and historical evidence for adjudication."
              }
            </p>
          </div>
        )}
      </div>
    </main>
  );
}
