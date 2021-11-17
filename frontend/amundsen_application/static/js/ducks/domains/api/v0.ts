import axios, { AxiosResponse } from 'axios'

import { Domains } from 'interfaces/Domains' 
import { DomainDetails } from 'interfaces/DomainsDetails'

export type DomainsAPI = {
    msg: string;
    domains: Domains[]
}

export type DomainDetailsAPI = {
    msg: string;
    domains: DomainDetails[]
}



export function getDomains() {
    return axios
        .get('/api/metadata/v0/domains')
        .then((resp: AxiosResponse<DomainsAPI>) => {
            return resp
        })
        .then((resp: AxiosResponse<DomainsAPI>) => resp.data.domains)
}

export function postDomains(body) {
    return axios
        .post('/api/metadata/v0/domains', (body) )
        .then((resp: AxiosResponse<DomainDetailsAPI>) => {
            return resp
        })
        .then((resp: AxiosResponse<DomainDetailsAPI>) => resp.data.domains)
}