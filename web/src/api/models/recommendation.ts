
export default interface Recommendation {
    document_id: number;
    similarity: number;
    title: string;
    url: string;
    published: string;
    author: string | null;
    image: string;
    thumbnail: string;
    summary: string;
    source_name: string;
    source_slug: string;
}
