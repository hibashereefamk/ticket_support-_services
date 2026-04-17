import React, { useEffect } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import "react-toastify/dist/ReactToastify.css";

const NotificationHandler = () => {
    useEffect(() => {
        const socket = new WebSocket('ws://localhost:8000/ws/notifications/');

        socket.onopen = () => {
            console.log("WebSocket Connected!");
        };

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);

            toast.info(data.message, {
                position: "top-right",
                autoClose: 5000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
            });
        };

        socket.onclose = () => {
            console.log("WebSocket Disconnected!");
        };

        return () => socket.close();
    }, []);

    return <ToastContainer />;
};

export default NotificationHandler;