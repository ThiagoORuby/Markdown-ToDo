
export type _Image = {
    id: number
    name: string
    url: string
}

export type _Document = {
    id: number
    title: string
    body: string
    images: _Image[]
    createdAt: string
    updatedAt: string
}