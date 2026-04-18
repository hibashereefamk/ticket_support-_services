import React, { useEffect } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import "react-toastify/dist/ReactToastify.css";

const NotificationHandler = () => {
 useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws/notifications/');

    socket.onopen = () => {
        console.log("✅ WebSocket Connected!");
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        toast.info(data.message);
    };

    socket.onclose = (e) => {
        console.log("❌ WebSocket Disconnected!");
    };

    return () => {
        // Only close if the socket is in an OPEN or CONNECTING state
        if (socket.readyState === 1 || socket.readyState === 0) {
            socket.close();
        }
    };
}, []);
};
export default NotificationHandler;