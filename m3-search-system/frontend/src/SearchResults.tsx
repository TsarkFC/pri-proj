import { ArquivoDoc, QueryResult } from "./query/Query";

export interface SearchResultsProps {
  result: QueryResult;
}

export const SearchResults = ({ result }: SearchResultsProps) => {
  return (
    <>
      <p>Found {result.response.numFound} results.</p>
      {result.response.docs.map((doc: ArquivoDoc, idx: number) => (
        <div key={idx}>
          <h2>
            <a href={doc["url"]}>{doc["article.title"]}</a>
          </h2>
          <p id="entities">
            {doc["article.entities.title"].map(
              (entity: string, idx: number, arr: Array<String>) => (
                <span key={idx} className="entity">
                  {entity}
                </span>
              )
            )}
          </p>
          <p dangerouslySetInnerHTML={{__html: doc["article.summary"]}}></p>
          <hr/>
        </div>
      ))}
    </>
  );
};
