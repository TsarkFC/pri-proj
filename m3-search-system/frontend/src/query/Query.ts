import axios, { AxiosResponse } from 'axios'

const executeQuery = (query: string) => {
    return axios.get(`http://localhost:3001/query/${encodeURIComponent(query)}`)
}

export const getAll: Query = () => executeQuery("q=*:*&defType=edismax")

export const getFullTextSearch: Query = (text?: string) => {
    const query = `q=${text}&defType=edismax&qf=article.title^3 article.entities.title^3 article.text article.summary article.publish_date`
    return executeQuery(query)
}

export type Query = (query?: string) => Promise<AxiosResponse<QueryResult, any>>

export interface ArquivoDoc {

}

export interface QueryResult {
    response: {
        numFound: number,
        docs: ArquivoDoc[]
    }
}
