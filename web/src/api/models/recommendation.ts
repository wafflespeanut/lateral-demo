
/** Some news recommendation returned by the API. */
export default interface Recommendation<Date> {
    document_id: number;
    similarity: number;
    title: string;
    url: string;
    published: Date;
    author: string | null;
    image: string | null;
    thumbnail: string | boolean;
    summary: string;
    source_name: string;
    source_slug: string;
}
