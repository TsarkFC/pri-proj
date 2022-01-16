import axios, { AxiosResponse } from "axios";

const executeQuery = (query: string) => {
  return axios.get(`http://localhost:3001/query/${encodeURIComponent(query)}`);
};

const addFacetsToQuery = (query: string) => {
  const facets = [
    "article.entities.title_facet",
    "article.authors_facet",
    // "article.publish_date",
    "newspaper",
  ];
  const str = facets.map((e) => `facet.field=${e}`).join("&");
  console.log(str)
  return `${query}&facet=true&${str}`;
};

export const getAll: Query = () => executeQuery("q=*:*&defType=edismax");

export const getFullTextSearch: Query = (text?: string) => {
  const query = `q=${text}&defType=edismax&qf=article.title^3 article.entities.title^3 article.text article.summary article.publish_date`;
  return executeQuery(addFacetsToQuery(query));
};

export type Query = (
  query?: string
) => Promise<AxiosResponse<QueryResult, any>>;

export interface ArquivoDoc {
  "article.authors": string;
  "article.entities.label": string[];
  "article.entities.title": string[];
  "article.image": string;
  "article.publish_date": string;
  "article.summary": string;
  "article.text": string;
  "article.title": string;
  id: string;
  newspaper: string;
  timestamp: string;
  url: string;
  urlkey: string;
}

export interface FacetFields {
  "article.entities.title_facet": any;
  "article.authors_facet": any;
  "newspaper": any;
}

export interface Facet {
  facet_queries: any;
  facet_fields: FacetFields;
  facet_ranges: any;
  facet_intervals: any;
  facet_heatmaps: any
}

export interface QueryResult {
  response: {
    numFound: number;
    docs: ArquivoDoc[];
  };
  facet_counts: Facet 
}
