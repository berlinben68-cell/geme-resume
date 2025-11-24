import React, { useState } from 'react';

const AdminDashboard = () => {
    // Mock Queue
    const [reviewQueue, setReviewQueue] = useState([
        { id: 101, user: "User_A", topic: "Microservices", code: "def init_service(): pass" },
        { id: 102, user: "User_B", topic: "React Hooks", code: "const useAuth = () => {}" }
    ]);

    const handleApprove = (id) => {
        console.log(`Approved commit ${id}`);
        setReviewQueue(reviewQueue.filter(item => item.id !== id));
    };

    const handleReject = (id) => {
        const reason = prompt("Enter rejection reason:");
        if (reason) {
            console.log(`Rejected commit ${id}. Reason: ${reason}`);
            setReviewQueue(reviewQueue.filter(item => item.id !== id));
        }
    };

    return (
        <div className="min-h-screen bg-gray-900 text-gray-300 font-mono p-8">
            <header className="mb-8 border-b border-gray-700 pb-4">
                <h1 className="text-2xl font-bold text-red-500">EXEC_GIT // ADMIN OVERWATCH</h1>
            </header>

            <div className="space-y-6">
                {reviewQueue.length === 0 ? (
                    <div className="text-center text-gray-500">Queue Empty. All systems nominal.</div>
                ) : (
                    reviewQueue.map((item) => (
                        <div key={item.id} className="bg-gray-800 border border-gray-700 p-6 rounded">
                            <div className="flex justify-between items-start mb-4">
                                <div>
                                    <h3 className="text-lg font-bold text-white">{item.user}</h3>
                                    <span className="text-xs bg-gray-700 px-2 py-1 rounded text-gray-400">{item.topic}</span>
                                </div>
                                <div className="space-x-2">
                                    <button
                                        onClick={() => handleReject(item.id)}
                                        className="px-4 py-2 bg-red-900 text-red-300 rounded hover:bg-red-800"
                                    >
                                        REJECT
                                    </button>
                                    <button
                                        onClick={() => handleApprove(item.id)}
                                        className="px-4 py-2 bg-green-900 text-green-300 rounded hover:bg-green-800"
                                    >
                                        APPROVE
                                    </button>
                                </div>
                            </div>

                            <div className="bg-black p-4 rounded border border-gray-800 overflow-x-auto">
                                <pre className="text-sm text-green-500">
                                    {item.code}
                                </pre>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default AdminDashboard;
