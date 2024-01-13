import { _Document } from "./entities";

export type User = {
    id: number
    username: string
    email: string
    createdAt: string
    documents: _Document[]
}