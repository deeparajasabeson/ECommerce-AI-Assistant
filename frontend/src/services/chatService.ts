import type { ChatApiResponse, ChatErrorPayload } from "../types/chat";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000"

export async function sendChatQuery(query: string): Promise<ChatApiResponse> {
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query })
        });

        if (!response.ok) {
            let message = "Failed to get a response from the assistant.";
            const responsesContentType = response.headers.get("content-type") ?? "";
            if(responsesContentType.includes("application/json")) {
                const payload = (await response.json()) as ChatErrorPayload;
                if (payload.detail) {
                    message = payload.detail;
                }                 
            } else {
                const fallbackText = await response.text();
                if (fallbackText) {
                    message = fallbackText;
                }
            }
            throw new Error(message);
        }
        return (await response.json()) as ChatApiResponse;
    } catch (error) {
        console.error("Error sending chat query:", error);
        throw error;
    }
}