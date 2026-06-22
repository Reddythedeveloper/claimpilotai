"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Activity, FileText, CheckCircle, AlertTriangle, Clock } from "lucide-react";
import Link from "next/link";

export default function Dashboard() {
  const [cases, setCases] = useState([
    { id: "CLM-100245", payer: "Aetna", amount: 8200.45, status: "pending", risk: 0.8 },
    { id: "CLM-100246", payer: "Cigna", amount: 450.00, status: "resolved", risk: 0.2 },
    { id: "CLM-100247", payer: "UHC", amount: 12500.00, status: "error", risk: 0.9 },
  ]);

  return (
    <main className="min-h-screen p-8 md:p-16 max-w-7xl mx-auto">
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between mb-12"
      >
        <div>
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
            ClaimPilot AI
          </h1>
          <p className="text-gray-400 mt-2">Revenue Cycle Intelligence Platform</p>
        </div>
        <button className="glass-button px-6 py-3 rounded-full font-semibold flex items-center gap-2">
          <Activity size={20} />
          New Case
        </button>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.1 }} className="glass-panel p-6">
          <div className="flex items-center gap-4 text-blue-400 mb-2">
            <FileText size={24} />
            <h3 className="font-semibold">Active Cases</h3>
          </div>
          <p className="text-3xl font-bold">1</p>
        </motion.div>
        <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.2 }} className="glass-panel p-6">
          <div className="flex items-center gap-4 text-purple-400 mb-2">
            <AlertTriangle size={24} />
            <h3 className="font-semibold">Revenue at Risk</h3>
          </div>
          <p className="text-3xl font-bold">$20,700</p>
        </motion.div>
        <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.3 }} className="glass-panel p-6">
          <div className="flex items-center gap-4 text-green-400 mb-2">
            <CheckCircle size={24} />
            <h3 className="font-semibold">Resolved Today</h3>
          </div>
          <p className="text-3xl font-bold">1</p>
        </motion.div>
      </div>

      <motion.h2 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="text-2xl font-semibold mb-6"
      >
        Queue Tracker
      </motion.h2>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="glass-panel overflow-hidden"
      >
        <table className="w-full text-left">
          <thead className="bg-white/5 border-b border-white/10">
            <tr>
              <th className="p-4 font-medium text-gray-300">Case ID</th>
              <th className="p-4 font-medium text-gray-300">Payer</th>
              <th className="p-4 font-medium text-gray-300">Amount</th>
              <th className="p-4 font-medium text-gray-300">Status</th>
              <th className="p-4 font-medium text-gray-300 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {cases.map((c) => (
              <tr key={c.id} className="hover:bg-white/5 transition-colors">
                <td className="p-4 font-mono text-sm text-blue-300">{c.id}</td>
                <td className="p-4">{c.payer}</td>
                <td className="p-4 font-mono">${c.amount.toFixed(2)}</td>
                <td className="p-4">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium flex items-center w-max gap-1
                    ${c.status === 'resolved' ? 'bg-green-500/20 text-green-400 border border-green-500/30' : ''}
                    ${c.status === 'pending' ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30' : ''}
                    ${c.status === 'error' ? 'bg-red-500/20 text-red-400 border border-red-500/30' : ''}
                  `}>
                    {c.status === 'pending' && <Clock size={12} />}
                    {c.status === 'resolved' && <CheckCircle size={12} />}
                    {c.status === 'error' && <AlertTriangle size={12} />}
                    {c.status.charAt(0).toUpperCase() + c.status.slice(1)}
                  </span>
                </td>
                <td className="p-4 text-right">
                  <Link href={`/cases/${c.id}`} className="text-sm text-blue-400 hover:text-blue-300 transition-colors">
                    Review Case &rarr;
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </motion.div>
    </main>
  );
}
