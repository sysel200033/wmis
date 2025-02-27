import request from './req';


export const apiGetMyself = () => request('GET', '/me');
export const apiUpdatePass = data => request('PUT', '/me/password', data);
export const apiDelateAccount = () => request('DELETE', '/me');