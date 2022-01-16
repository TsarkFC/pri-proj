import { ArquivoDoc, QueryResult } from "./query/Query";

export interface SearchResultsProps {
  result: QueryResult;
}

export const SearchFilters = ({ result }: SearchResultsProps) => {
  const facet_fields = result.facet_counts.facet_fields;
  const temp_fields = [
    facet_fields["article.authors_facet"],
    facet_fields["article.entities.title_facet"],
    facet_fields.newspaper,
  ];
  const titles = [
    "Autores",
    "Entidades",
    "Jornais"
  ]
  const fields: any[] = [];

  temp_fields.forEach((a) => {
    let res: (string|number)[][] = [];

    for (let i = 0; i < a.length && i < 10; i += 2) {
      const facet: string = a[i]
      const num: number = a[i+1]
      res.push([facet, num]);
    }
    fields.push(res)
  });

  let i = 0;
  return (
    <>
      <p>Filters</p>
      {fields.map((field: any, idx: number) => (
        <div key={idx}>
          <h3>{titles[i++]}</h3>
          {field.map((a: any[], idx: number) => (
            <p key={idx}>Field: {a[0]} Count: {a[1]}</p>
          ))}
        </div>
      ))}
    </>
  );
};
