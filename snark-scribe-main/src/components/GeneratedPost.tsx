import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Copy, Check } from "lucide-react";
import { useState } from "react";
import { useToast } from "@/hooks/use-toast";

interface GeneratedPostProps {
  post: string;
}

const GeneratedPost = ({ post }: GeneratedPostProps) => {
  const [copied, setCopied] = useState(false);
  const { toast } = useToast();

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(post);
      setCopied(true);
      toast({
        title: "Copied!",
        description: "Post copied to clipboard",
      });
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      toast({
        title: "Failed to copy",
        description: "Please try again",
        variant: "destructive",
      });
    }
  };

  return (
    <Card className="p-8 shadow-[var(--shadow-elegant)] border-2 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-semibold">Your Masterpiece</h3>
          <Button
            variant="outline"
            size="sm"
            onClick={handleCopy}
            className="gap-2"
          >
            {copied ? (
              <>
                <Check className="w-4 h-4" />
                Copied
              </>
            ) : (
              <>
                <Copy className="w-4 h-4" />
                Copy
              </>
            )}
          </Button>
        </div>
        
        <div className="bg-muted/50 rounded-lg p-6 min-h-[200px]">
          <div className="prose prose-sm max-w-none">
            <p className="whitespace-pre-wrap text-foreground leading-relaxed">
              {post}
            </p>
          </div>
        </div>
        
        <p className="text-xs text-muted-foreground text-center italic">
          Disclaimer: This is satire. Use responsibly (or don't, we're not your boss).
        </p>
      </div>
    </Card>
  );
};

export default GeneratedPost;
