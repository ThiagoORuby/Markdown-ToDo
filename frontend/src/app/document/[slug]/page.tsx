


export default function Document({params} : {
    params: {
        slug: string
    }}) {
    return (
        <div>
            Document {params.slug}
        </div>
    )
}