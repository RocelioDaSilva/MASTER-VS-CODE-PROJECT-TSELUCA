import { GoogleGenAI } from "@google/genai";
import { SuitabilityResult, Community, MCDAWeights } from "../types";
import { ANGOLA_COMMUNITIES } from "../constants";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY || "" });

export async function getEnergyInsights(results: SuitabilityResult[], weights: MCDAWeights) {
  const topCommunities = results
    .sort((a, b) => b.score - a.score)
    .slice(0, 3)
    .map(r => {
      const c = ANGOLA_COMMUNITIES.find(com => com.id === r.communityId);
      return `${c?.name} (${r.score.toFixed(1)}%, LCOE: $${r.lcoe.toFixed(3)})`;
    });

  const prompt = `
    As an energy policy expert for Angola, analyze these solar suitability results:
    
    Top 3 Communities: ${topCommunities.join(", ")}
    Current Weights: Climate: ${weights.climate}, Soil: ${weights.soil}, Terrain: ${weights.terrain}, Infrastructure: ${weights.infrastructure}
    
    Provide a brief (3-4 sentences) strategic insight on why these communities are leading and what policy recommendations you would make for rural electrification in these areas.
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: prompt,
    });
    return response.text;
  } catch (error) {
    console.error("Gemini Error:", error);
    return "Unable to generate AI insights at this time.";
  }
}
