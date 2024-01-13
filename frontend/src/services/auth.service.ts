import { User } from '@/types/user';
import axios, { Axios, AxiosInstance } from 'axios';
import Cookies from 'js-cookie';

export class AuthService{
    protected readonly instance: AxiosInstance;
    public constructor(url: string) {
        this.instance = axios.create({
            baseURL: url,
        });
    }

    login = async (username: string, password: string) => {
        return await this.instance.post('/auth/login', {
            username,
            password
        }, {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "credentials": "include"
              },
        })
        .then((res) => {
            return res.data;
        })
    }

    getMe = async (token: string) => {
        return await this.instance.get('/auth/me', {
            headers: {
                Authorization: `Bearer ${token || ""}`
            },
        })
        .then((res) => {
            return res.data as User
        }).catch((err) => {
            return null
        })}

    logout = async () => {
        return await this.instance.get('/auth/logout', {}).then((res) => {
            return res.data
        })
    }}