import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Search, Loader2, FileText, Activity, Terminal as TerminalIcon } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';

const API_BASE = 'http://localhost:8000';

function App() {
  const [target, setTarget] = useState('');
  const [taskId, setTaskId] = useState(null);
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const logsEndRef = useRef(null);

  useEffect(() => {
    let interval;
    if (taskId && status?.status !== 'completed' && status?.status !== 'failed') {
      interval = setInterval(async () => {
        try {
          const res = await axios.get(`${API_BASE}/status/${taskId}`);
          setStatus(res.data);
          if (res.data.status === 'completed') {
            setReport(res.data.report);
            clearInterval(interval);
          }
        } catch (err) {
          console.error(err);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [taskId, status]);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [status?.logs]);

  const handleResearch = async () => {
    if (!target) return;
    setLoading(true);
    setReport(null);
    setStatus(null);
    try {
      const res = await axios.post(`${API_BASE}/research`, { target });
      setTaskId(res.data.task_id);
    } catch (err) {
      alert("Backend error! Make sure backend/api.py is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-8 max-w-6xl mx-auto">
      <header className="text-center mb-12">
        <motion.h1 
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="text-6xl font-black mb-4 tracking-tight"
          style={{ fontFamily: 'Outfit, sans-serif' }}
        >
          OPEN<span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-cyan-400">CLAW</span>
        </motion.h1>
        <p className="text-gray-400 text-lg">Autonomous AI Research Agent</p>
      </header>

      <div className="flex flex-col gap-8">
        {/* Input Section */}
        <motion.div 
          className="glass-panel p-8 flex flex-col md:flex-row items-center justify-center gap-4"
          whileHover={{ scale: 1.01 }}
        >
          <div className="relative flex-1 w-full max-w-md">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" size={20} />
            <input 
              type="text" 
              placeholder="Enter person name (e.g. Sam Altman)"
              className="pl-12"
              value={target}
              onChange={(e) => setTarget(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleResearch()}
            />
          </div>
          <button 
            className="glow-button flex items-center gap-2"
            onClick={handleResearch}
            disabled={loading || (taskId && status?.status === 'running')}
          >
            {loading ? <Loader2 className="animate-spin" /> : <Activity size={20} />}
            Start Research
          </button>
        </motion.div>

        {/* Status & Terminal Section */}
        <AnimatePresence>
          {taskId && (
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="grid grid-cols-1 md:grid-cols-2 gap-8"
            >
              <div className="glass-panel p-6">
                <h3 className="flex items-center gap-2 mb-4 font-bold text-gray-300">
                  <TerminalIcon size={18} /> ReAct Loop Log
                </h3>
                <div className="terminal-box">
                  {status?.logs?.map((log, i) => (
                    <div key={i} className="mb-1">{log}</div>
                  ))}
                  {!status?.logs?.length && <div className="text-gray-600 italic">Starting engine...</div>}
                  <div ref={logsEndRef} />
                </div>
              </div>

              <div className="glass-panel p-6 flex flex-col justify-center items-center text-center">
                <div className="text-sm uppercase tracking-widest text-gray-500 mb-2">Research Status</div>
                <div className="text-3xl font-bold mb-4 uppercase tabular-nums">
                  {status?.status || 'initializing'}
                </div>
                {status?.status === 'running' && (
                  <div className="w-full bg-gray-800 rounded-full h-2 mb-4">
                    <motion.div 
                      className="bg-purple-500 h-2 rounded-full"
                      animate={{ width: ['0%', '100%'] }}
                      transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
                    />
                  </div>
                )}
                {status?.status === 'completed' && <Activity className="text-green-500 animate-pulse" size={48} />}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Report Section */}
        <AnimatePresence>
          {report && (
            <motion.div 
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              className="glass-panel p-10 report-container"
            >
              <h2 className="flex items-center gap-2 text-3xl font-bold mb-8 border-b border-gray-800 pb-4">
                <FileText className="text-purple-400" /> Final Research Report
              </h2>
              <ReactMarkdown>{report}</ReactMarkdown>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <footer className="text-center mt-20 text-gray-600 text-sm">
        Powered by OpenClaw Architecture & Groq
      </footer>
    </div>
  );
}

export default App;
