"use client";
import React, { useState, useCallback } from 'react';
import { Upload, X, FileCheck, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface UploadFile {
  id: string;
  file: File;
  progress: number;
  status: 'uploading' | 'processing' | 'completed' | 'error';
}

export default function UploadZone() {
  const [files, setFiles] = useState<UploadFile[]>([]);
  const [isDragging, setIsDragging] = useState(false);

  const handleUpload = (selectedFiles: FileList | null) => {
    if (!selectedFiles) return;
    
    const newFiles = Array.from(selectedFiles).map(file => ({
      id: Math.random().toString(36).substring(7),
      file,
      progress: 0,
      status: 'uploading' as const
    }));

    setFiles(prev => [...newFiles, ...prev]);

    // Simulate Upload & AI Processing Pipeline
    newFiles.forEach(f => simulateProcess(f.id));
  };

  const simulateProcess = (id: string) => {
    setTimeout(() => {
      setFiles(prev => prev.map(f => f.id === id ? { ...f, progress: 100, status: 'processing' } : f));
      setTimeout(() => {
        setFiles(prev => prev.map(f => f.id === id ? { ...f, status: 'completed' } : f));
      }, 2000);
    }, 1500);
  };

  return (
    <div className="w-full space-y-4">
      <div 
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={(e) => { e.preventDefault(); setIsDragging(false); handleUpload(e.dataTransfer.files); }}
        className={`border-2 border-dashed rounded-3xl p-12 transition-all duration-200 flex flex-col items-center justify-center cursor-pointer
          ${isDragging ? 'border-brand-500 bg-brand-50/50' : 'border-slate-200 hover:border-brand-300 hover:bg-slate-50'}`}
      >
        <div className="p-4 bg-brand-100 rounded-full mb-4">
          <Upload className="w-8 h-8 text-brand-600" />
        </div>
        <h3 className="text-xl font-semibold text-slate-900">Upload high-res assets</h3>
        <p className="text-slate-500 mt-2 text-center max-w-sm">
          Drag and drop images or videos. Our AI will automatically generate keywords, titles, and SEO descriptions.
        </p>
        <input 
          type="file" 
          multiple 
          className="hidden" 
          id="file-upload" 
          onChange={(e) => handleUpload(e.target.files)}
        />
        <label htmlFor="file-upload" className="mt-6 px-6 py-2.5 bg-brand-600 text-white rounded-xl font-medium hover:bg-brand-700 transition-colors">
          Select Files
        </label>
      </div>

      <div className="space-y-3">
        <AnimatePresence>
          {files.map((file) => (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95 }}
              key={file.id} 
              className="bg-white border border-slate-200 p-4 rounded-xl flex items-center gap-4"
            >
              <div className="w-12 h-12 bg-slate-100 rounded-lg flex items-center justify-center flex-shrink-0">
                {file.file.type.startsWith('image') ? '🖼️' : '🎥'}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex justify-between mb-1">
                  <p className="text-sm font-medium text-slate-900 truncate">{file.file.name}</p>
                  <span className="text-xs font-semibold uppercase tracking-wider">
                    {file.status === 'uploading' && <span className="text-blue-500">Uploading</span>}
                    {file.status === 'processing' && <span className="text-amber-500 flex items-center gap-1"><Loader2 className="w-3 h-3 animate-spin"/> AI Analyzing</span>}
                    {file.status === 'completed' && <span className="text-emerald-500 flex items-center gap-1"><FileCheck className="w-3 h-3"/> Ready</span>}
                  </span>
                </div>
                <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                  <motion.div 
                    initial={{ width: 0 }}
                    animate={{ width: file.status === 'completed' ? '100%' : `${file.progress}%` }}
                    className={`h-full ${file.status === 'completed' ? 'bg-emerald-500' : 'bg-brand-500'}`}
                  />
                </div>
              </div>
              <button 
                onClick={() => setFiles(prev => prev.filter(f => f.id !== file.id))}
                className="p-1 hover:bg-slate-100 rounded-md text-slate-400"
              >
                <X className="w-5 h-5" />
              </button>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}