import express from 'express'
import { env } from 'process'
import { createClient } from 'solr-client'
import cors from 'cors'

const app = express();
const PORT = env.PORT;

app.use(cors())

const client = createClient({
    port: 8983,
    host: "solr",
    core: "arquivo",
    path: "/solr"
})

app.get('/query/:query', async (req, res) => {
    const query = req.params.query
        .split("&")
        .map(part => part
                        .split("=")
                        .map(subpart => encodeURIComponent(subpart))
                        .join("="))
        .join("&")

    console.log(query)

    const response = await client.doQuery('query', query)
    res.send(response)
})

app.listen(PORT, () => {
    console.log(`SOLR interface running on http://localhost:${PORT}`)
})
