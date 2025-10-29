import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card } from "@/components/ui/card";
import { Sparkles, Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { generatePost } from "@/services/api";
import PostTypeSelector from "@/components/PostTypeSelector";
import GeneratedPost from "@/components/GeneratedPost";
import VideoUpload from "@/components/VideoUpload";
import Scene3D from "@/components/Scene3D";

type PostType = "performative" | "serious" | "cluely" | "boardy";

const Index = () => {
  const [postType, setPostType] = useState<PostType>("performative");
  const [context, setContext] = useState("");
  const [generatedPost, setGeneratedPost] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const { toast } = useToast();

  const handleGenerate = async () => {
    if (!context.trim()) {
      toast({
        title: "Missing input",
        description: "Please provide some context",
        variant: "destructive",
      });
      return;
    }

    setIsGenerating(true);
    setGeneratedPost("");

    try {
      const result = await generatePost({
        postType,
        context: context.trim(),
      });

      if (result?.post) {
        setGeneratedPost(result.post);
      } else {
        throw new Error("No post generated");
      }
    } catch (error: any) {
      console.error("Generation error:", error);
      toast({
        title: "Generation failed",
        description: error.message || "Failed to generate post. Make sure the backend server is running.",
        variant: "destructive",
      });
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted relative">
      <Scene3D postType={postType} />
      {/* Hero Section */}
      <div className="relative z-10 overflow-hidden animate-fade-in">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-accent/5" />
        <div className="container mx-auto px-4 py-16 relative">
          <div className="max-w-3xl mx-auto text-center space-y-6">
            <div className="inline-block animate-scale-in">
              <div className="flex items-center gap-2 bg-primary/10 rounded-full px-4 py-2 mb-4">
                <Sparkles className="w-4 h-4 text-primary animate-pulse" />
                <span className="text-sm font-medium text-primary">AI-Powered Satire</span>
              </div>
            </div>
            <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent leading-tight">
              LinkedIn Post Generator
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Create hilariously authentic sarcastic LinkedIn posts. Choose your cringe level and let AI do the rest.
            </p>
          </div>
        </div>
      </div>

      {/* Generator Section */}
      <div className="container mx-auto px-4 pb-20 relative">
        <div className="max-w-4xl mx-auto space-y-8">
          {/* Input Card */}
          <Card className="p-8 shadow-[var(--shadow-elegant)] border-2 hover:shadow-[var(--shadow-glow)] transition-shadow duration-300">
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-semibold mb-6">Create Your Post</h2>
                <PostTypeSelector value={postType} onChange={setPostType} />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Context (Optional)</label>
                <Textarea
                  placeholder="Add some context about what you want to say... or don't, the AI will improvise."
                  value={context}
                  onChange={(e) => setContext(e.target.value)}
                  className="min-h-[120px] resize-none"
                />
              </div>

              <Button
                onClick={handleGenerate}
                disabled={isGenerating}
                className="w-full h-12 text-lg font-semibold shadow-lg hover:shadow-xl transition-all"
                size="lg"
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Generating Cringe...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5 mr-2" />
                    Generate Post
                  </>
                )}
              </Button>
            </div>
          </Card>

          {/* Generated Post */}
          {generatedPost && <GeneratedPost post={generatedPost} />}

          {/* Video Upload & Analysis */}
          <VideoUpload />

          {/* Examples Section */}
          <div className="mt-16 pt-8 border-t">
            <h3 className="text-2xl font-semibold mb-6 text-center">How It Works</h3>
            <div className="grid md:grid-cols-3 gap-6">
              <Card className="p-6 text-center space-y-3">
                <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mx-auto">
                  <span className="text-2xl font-bold text-primary">1</span>
                </div>
                <h4 className="font-semibold">Choose Your Style</h4>
                <p className="text-sm text-muted-foreground">
                  Pick from Performative, Serious, Cluely, or Boardy
                </p>
              </Card>
              <Card className="p-6 text-center space-y-3">
                <div className="w-12 h-12 rounded-full bg-accent/10 flex items-center justify-center mx-auto">
                  <span className="text-2xl font-bold text-accent">2</span>
                </div>
                <h4 className="font-semibold">Add Context</h4>
                <p className="text-sm text-muted-foreground">
                  Optional text and media for better results
                </p>
              </Card>
              <Card className="p-6 text-center space-y-3">
                <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mx-auto">
                  <span className="text-2xl font-bold text-primary">3</span>
                </div>
                <h4 className="font-semibold">Generate & Share</h4>
                <p className="text-sm text-muted-foreground">
                  Get your perfectly cringe post instantly
                </p>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
