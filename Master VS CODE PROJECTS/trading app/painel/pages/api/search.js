import { MongoClient } from 'mongodb';

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb+srv://SEU_USUARIO:SUA_SENHA@cluster0.xxxxx.mongodb.net/intermediario';
const DB_NAME = process.env.DB_NAME || 'intermediario';
const COLLECTION_OFFERS = 'ofertas';

export default async function handler(req, res) {
  const { q } = req.query;

  if (!q) {
    return res.status(400).json({ error: 'Query é obrigatória' });
  }

  let client;
  try {
    client = new MongoClient(MONGODB_URI);
    await client.connect();
    const db = client.db(DB_NAME);
    const collection = db.collection(COLLECTION_OFFERS);

    const offers = await collection
      .find({ 
        content: { $regex: q, $options: 'i' }
      })
      .sort({ timestamp: -1 })
      .limit(50)
      .toArray();

    res.status(200).json(offers);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Erro ao buscar no banco de dados: ' + err.message });
  } finally {
    if (client) {
      await client.close();
    }
  }
}
