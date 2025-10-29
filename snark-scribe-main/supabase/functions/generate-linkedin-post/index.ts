import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { postType, context, hasFile } = await req.json();
    const LOVABLE_API_KEY = Deno.env.get("LOVABLE_API_KEY");

    if (!LOVABLE_API_KEY) {
      throw new Error("LOVABLE_API_KEY is not configured");
    }

    // Create the system prompt based on post type
    const systemPrompts = {
      performative: `You are a master of performative LinkedIn posts. Create posts that are:
- Full of humble brags disguised as gratitude
- Mention "blessed" or "grateful" multiple times
- Include unnecessary emojis
- Turn simple achievements into epic journeys
- Name-drop companies or people
- End with vague inspirational advice
- Use phrases like "I'm humbled to announce" when clearly not humble
- Include hashtags like #leadership #growth #blessed`,
      
      serious: `You are a master of overly serious corporate LinkedIn posts. Create posts that:
- Use maximum business jargon and buzzwords
- Include phrases like "synergy", "paradigm shift", "disrupt", "leverage", "circle back"
- Take simple concepts and make them unnecessarily complex
- Reference "thought leadership" and "best practices"
- Include statistics that sound impressive but are meaningless
- Use corporate speak like "moving the needle" and "low-hanging fruit"
- End with a call to "connect" or "engage in the conversation"`,
      
      cluely: `You are a master of clueless LinkedIn posts. Create posts that:
- Show complete misunderstanding of current trends or technology
- Include outdated references thinking they're cutting edge
- Mix up terminology incorrectly
- Make confidently wrong statements
- Show lack of awareness about how things actually work
- Use technology terms incorrectly
- Display tone-deaf takes on serious topics
- Include cringe attempts at being relatable to younger generations`,
      
      boardy: `You are a master of corporate "boardroom culture" LinkedIn posts. Create posts that:
- Obsess over meetings, synergies, and alignment
- Use phrases like "let's take this offline", "circle back", "touch base"
- Mention quarterly reviews, stakeholder buy-in, and deliverables
- Reference pointless meetings that could have been emails
- Include calendar screenshots showing back-to-back meetings as a flex
- Talk about "meeting fatigue" while scheduling more meetings
- Use corporate meeting jargon like "parking lot ideas" and "action items"
- Celebrate meaningless corporate rituals and ceremonies`,
    };

    const systemPrompt = systemPrompts[postType as keyof typeof systemPrompts];
    
    let userPrompt = `Generate a sarcastic, satirical LinkedIn post in the ${postType} style.`;
    
    if (context) {
      userPrompt += ` Context: ${context}`;
    }
    
    if (hasFile) {
      userPrompt += ` The user has uploaded an image/video to accompany this post (describe what might be in it based on the context, or imagine something appropriately cringe for a ${postType} post).`;
    }
    
    userPrompt += ` Make it authentically cringe-worthy and recognizable as LinkedIn satire. Keep it between 100-200 words. Use line breaks and emojis appropriately for the style.`;

    const response = await fetch("https://ai.gateway.lovable.dev/v1/chat/completions", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${LOVABLE_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "google/gemini-2.5-flash",
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: userPrompt },
        ],
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("AI Gateway error:", response.status, errorText);
      throw new Error(`AI Gateway error: ${response.status}`);
    }

    const data = await response.json();
    const generatedPost = data.choices?.[0]?.message?.content;

    if (!generatedPost) {
      throw new Error("No content generated");
    }

    return new Response(
      JSON.stringify({ post: generatedPost }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (error) {
    console.error("Error generating post:", error);
    const errorMessage = error instanceof Error ? error.message : "Failed to generate post";
    return new Response(
      JSON.stringify({ error: errorMessage }),
      {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      }
    );
  }
});
