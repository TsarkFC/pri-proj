import axios, { AxiosResponse } from "axios";

const executeQuery = (query: string) => {
  return axios.get(`http://localhost:3001/query/${encodeURIComponent(query)}`);
};

const facetFields = [
  "article.authors_facet",
  "article.entities.title_facet",
  "newspaper",
  // "article.publish_date",
];

const filterFields = [
  "article.authors",
  "article.entities.title",
  "newspaper"
]

const addFacetsToQuery = (query: string) => {
  const str = facetFields.map((e) => `facet.field=${e}`).join("&");
  return `${query}&facet=true&${str}`;
};

const addFiltersToQuery = (query: string, filters: string[][]) => {
  let str = query;
  console.log(filters);
  for (let i = 0; i < filters?.length; i++) {
    console.log(i, filterFields[i]);
    filters[i].forEach((facetValue) => {
      if (facetValue != "") str += `&fq=${filterFields[i]}:${facetValue}`;
    });
  }
  return str;
};

export const getAll: Query = () => executeQuery("q=*:*&defType=edismax");

export const buildQuery = (text: string, filters?: string[][]) => {
  const query = `q=${text}&defType=edismax&qf=article.title^3 article.entities.title^3 article.text article.summary article.publish_date`;
  return filters ? addFiltersToQuery(query, filters) : addFacetsToQuery(query);
};

export const getFullTextSearch: Query = (text?: string) => {
  const def =
    "q=&defType=edismax&qf=article.title^3 article.entities.title^3 article.text article.summary article.publish_date";
  return executeQuery(text ? text : def);
};

export const parseFacets = (result: QueryResult) => {
  if (result.facet_counts) {
    const facetFields = result.facet_counts.facet_fields;
    const rawFields = [
      facetFields["article.authors_facet"],
      facetFields["article.entities.title_facet"],
      facetFields.newspaper,
    ];

    const parsedFields: any[] = [];
    rawFields.forEach((a) => {
      let res: (string | number)[][] = [];

      for (let i = 0; i < a.length && i < 10; i += 2) {
        const facet: string = a[i];
        const num: number = a[i + 1];
        res.push([facet, num]);
      }
      parsedFields.push(res);
    });
    return parsedFields;
  }
  return [];
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
  newspaper: any;
}

export interface Facet {
  facet_queries: any;
  facet_fields: FacetFields;
  facet_ranges: any;
  facet_intervals: any;
  facet_heatmaps: any;
}

export interface QueryResult {
  response: {
    numFound: number;
    docs: ArquivoDoc[];
  };
  facet_counts: Facet;
}
