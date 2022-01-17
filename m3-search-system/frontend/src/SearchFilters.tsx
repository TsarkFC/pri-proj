import { useState } from "react";
import { QueryResult, getFullTextSearch } from "./query/Query";

export interface SearchResultsProps {
  fields: any[];
  runQuery: any;
}

export const SearchFilters = ({ fields, runQuery }: SearchResultsProps) => {
  const [selectedFacetFields] = useState([[""], [""], [""]]);
  const titles = ["Autores", "Entidades", "Jornais"];

  let i = 0;
  return (
    <>
      <p>Filters</p>
      {fields.map((field: any, idx: number) => (
        <div key={idx}>
          <h3>{titles[i++]}</h3>
          <form>
            {field.map((facet: any[], idx: number) => (
              <div key={idx}>
                <label htmlFor={titles[i - 1] + idx}>
                  {facet[0]} ({facet[1]})
                  <input
                    id={titles[i - 1] + idx}
                    type="checkbox"
                    data-facet={i - 1}
                    onChange={(event) => {
                      const facetPos = event.target.dataset.facet;
                      if (facetPos) {
                        const pos: number = +facetPos;
                        if (event.target.checked)
                          selectedFacetFields[pos].push(facet[0]);
                        else {
                          console.log("UNCHECK")
                          selectedFacetFields[pos] = selectedFacetFields[pos].filter((e) => {
                            console.log(e, facet[0], e !== facet[0])
                            return e !== facet[0]
                          })
                          
                        }
                        console.log(selectedFacetFields)
                        runQuery(getFullTextSearch, selectedFacetFields);
                      }
                    }}
                  />
                </label>
                <br></br>
              </div>
            ))}
          </form>
        </div>
      ))}
    </>
  );
};
