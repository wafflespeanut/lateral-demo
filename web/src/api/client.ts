import Message from "./models/message";

export default interface ApiClient {
    /**
     * Fetches the current datetime from the server.
     */
    getServerTime(): Promise<Date>;
}

class HttpApiClient implements ApiClient {

    private basePath: string = '/api'

    async getServerTime(): Promise<Date> {
        const response = await fetch(this.basePath);
        const json: Message<string> = await response.json();
        return new Date(json.message);
    }
}

export { HttpApiClient };
