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

    login = (username: string, password: string) => {
        return this.instance.post('/auth/login', {
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

    getMe = (token: string) => {
        return this.instance.get('/auth/me', {
            headers: {
                Authorization: `Bearer ${token || ""}`
            },
        })
        .then((res) => {
            return res.data as User
        }).catch((err) => {
            return null
        })}

    logout = () => {
        return this.instance.get('/auth/logout', {}).then((res) => {
            return res.data
        })
    }}