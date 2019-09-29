import Message from "./models/message";
import Recommendation from "./models/recommendation";

/** Client interface for the API. */
export default interface ApiClient {
    /**
     * Fetches the current datetime from the server.
     */
    getServerTime(): Promise<Date>;

    /**
     * Fetches the recommendations similar to the given text.
     *
     * @param text Text to query the API.
     */
    getSimilarNews(text: string): Promise<Array<Recommendation<Date>>>;
}

/** Actual HTTP client backed by the fetch API. */
class HttpApiClient implements ApiClient {

    private basePath: string = '/api'

    async getServerTime(): Promise<Date> {
        const response = await fetch(this.basePath);
        const json: Message<string> = await response.json();
        return new Date(json.message);
    }

    async getSimilarNews(text: string): Promise<Array<Recommendation<Date>>> {
        const response = await fetch(`${this.basePath}/recommendations`, {
            method: 'POST',
            body: JSON.stringify({ text }),
            headers: {
                'Content-Type': 'application/json',
            },
        });
        const json: Array<Recommendation<string>> = await response.json();
        return json.map(r => {
            // It's better to type-cast because we only want to change that one field.
            const record = (r as any) as Recommendation<Date>;
            record.published = new Date(record.published);
            return record;
        })
    }
}

export { HttpApiClient };
