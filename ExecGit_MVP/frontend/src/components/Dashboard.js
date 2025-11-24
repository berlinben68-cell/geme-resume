import React, { useState } from 'react';
// Assuming Tailwind CSS is configured in the project

const Dashboard = () => {
    const [stealthMode, setStealthMode] = useState(false);

    // Mock Data
    const dnaMatchScore = 98;
    const pendingApprovals = [
        { id: 1, message: "Refactor auth middleware for lower latency", files: ["auth.py", "middleware.py"] },
        { id: 2, message: "Add zero-knowledge proof demo", files: ["zk_demo.py"] },
        { id: 3, message: "Optimize database connection pool", files: ["db.py"] }
    ];
    const growthData = [10, 25, 40, 55, 80, 120]; // Mock views/stars over time

    return (
        <div className="min-h-screen bg-gray-900 text-green-400 font-mono p-8">
            {/* Header */}
            <header className="flex justify-between items-center mb-12 border-b border-green-800 pb-4">
                <h1 className="text-3xl font-bold tracking-wider">EXEC_GIT // DASHBOARD</h1>
                <div className="flex items-center space-x-4">
                    <span className="text-sm text-gray-400">STATUS:</span>
                    <button
                        onClick={() => setStealthMode(!stealthMode)}
                        className={`px-4 py-2 rounded border ${stealthMode ? 'bg-gray-800 text-gray-500 border-gray-600' : 'bg-green-900 text-green-300 border-green-500 animate-pulse'}`}
                    >
                        {stealthMode ? "PAUSE ACTIVITY" : "ACTIVE GHOSTWRITING"}
                    </button>
                </div>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">

                {/* 1. DNA Match Visualizer */}
                <div className="bg-gray-800 border border-green-700 p-6 rounded-lg shadow-lg shadow-green-900/20">
                    <h2 className="text-xl mb-4 flex items-center">
                        <span className="mr-2">🧬</span> CODE DNA MATCH
                    </h2>
                    <div className="relative pt-1">
                        <div className="flex mb-2 items-center justify-between">
                            <div>
                                <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-green-900 bg-green-400">
                                    Authenticity
                                </span>
                            </div>
                            <div className="text-right">
                                <span className="text-xs font-semibold inline-block text-green-400">
                                    {dnaMatchScore}%
                                </span>
                            </div>
                        </div>
                        <div className="overflow-hidden h-4 mb-4 text-xs flex rounded bg-gray-700 border border-gray-600">
                            <div style={{ width: `${dnaMatchScore}%` }} className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-green-500"></div>
                        </div>
                        <p className="text-sm text-gray-400">
                            The AI is currently replicating your indentation style, variable naming, and comment frequency with high precision.
                        </p>
                    </div>
                </div>

                {/* 2. Growth Graph (Mock Visual) */}
                <div className="bg-gray-800 border border-green-700 p-6 rounded-lg shadow-lg shadow-green-900/20">
                    <h2 className="text-xl mb-4 flex items-center">
                        <span className="mr-2">📈</span> GROWTH GRAPH
                    </h2>
                    <div className="h-32 flex items-end space-x-2 border-b border-l border-gray-600 p-2">
                        {growthData.map((val, idx) => (
                            <div key={idx} style={{ height: `${val}%` }} className="w-full bg-green-600 opacity-80 hover:opacity-100 transition-all duration-300"></div>
                        ))}
                    </div>
                    <div className="flex justify-between text-xs text-gray-500 mt-2">
                        <span>Week 1</span>
                        <span>Week 6</span>
                    </div>
                </div>

                {/* 3. Pending Approvals */}
                <div className="col-span-1 md:col-span-2 bg-gray-800 border border-green-700 p-6 rounded-lg shadow-lg shadow-green-900/20">
                    <h2 className="text-xl mb-4 flex items-center">
                        <span className="mr-2">🛡️</span> PENDING APPROVALS
                    </h2>
                    <div className="space-y-4">
                        {pendingApprovals.map((item) => (
                            <div key={item.id} className="flex justify-between items-center bg-gray-900 p-4 rounded border border-gray-700 hover:border-green-500 transition-colors">
                                <div>
                                    <h3 className="font-bold text-green-300">{item.message}</h3>
                                    <p className="text-xs text-gray-500">Files: {item.files.join(", ")}</p>
                                </div>
                                <div className="flex space-x-2">
                                    <button className="px-3 py-1 text-xs border border-red-500 text-red-500 rounded hover:bg-red-900">REJECT</button>
                                    <button className="px-3 py-1 text-xs bg-green-700 text-white rounded hover:bg-green-600">APPROVE & PUSH</button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

            </div>
        </div>
    );
};

export default Dashboard;
