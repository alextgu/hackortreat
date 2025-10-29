import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Video, Upload, Loader2, CheckCircle2, AlertCircle } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { uploadVideo, getVideoAnalysis, type VideoAnalysis } from "@/services/api";

const VideoUpload = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadedFilename, setUploadedFilename] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<VideoAnalysis | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const { toast } = useToast();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      // Check file size (100MB limit for Gemini)
      if (selectedFile.size > 100 * 1024 * 1024) {
        toast({
          title: "File too large",
          description: "Please select a video smaller than 100MB",
          variant: "destructive",
        });
        return;
      }
      setFile(selectedFile);
      setAnalysis(null);
      setUploadedFilename(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    setAnalysis(null);

    try {
      const result = await uploadVideo(file);
      setUploadedFilename(result.filename);
      
      toast({
        title: "Video uploaded!",
        description: "AI analysis in progress...",
      });

      // Poll for analysis results
      if (result.analysis_pending) {
        setIsAnalyzing(true);
        pollForAnalysis(result.filename);
      }
    } catch (error: any) {
      console.error("Upload error:", error);
      toast({
        title: "Upload failed",
        description: error.message || "Failed to upload video. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsUploading(false);
    }
  };

  const pollForAnalysis = async (filename: string, attempt = 0) => {
    const maxAttempts = 30; // Max 30 attempts (30 seconds)
    
    if (attempt >= maxAttempts) {
      setIsAnalyzing(false);
      toast({
        title: "Analysis timeout",
        description: "Video analysis is taking longer than expected. Check back later.",
        variant: "destructive",
      });
      return;
    }

    try {
      await new Promise(resolve => setTimeout(resolve, 1000)); // Wait 1 second
      const analysisResult = await getVideoAnalysis(filename);
      setAnalysis(analysisResult);
      setIsAnalyzing(false);
      
      toast({
        title: "Analysis complete!",
        description: "Your video has been analyzed by AI",
      });
    } catch (error: any) {
      // If analysis not ready, try again
      if (error.message.includes('not ready')) {
        pollForAnalysis(filename, attempt + 1);
      } else {
        console.error("Analysis error:", error);
        setIsAnalyzing(false);
      }
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024 * 1024) {
      return `${(bytes / 1024).toFixed(1)} KB`;
    }
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <Card className="p-8 shadow-[var(--shadow-elegant)] border-2">
      <div className="space-y-6">
        <div className="flex items-center gap-3">
          <Video className="w-6 h-6 text-primary" />
          <h2 className="text-2xl font-semibold">Video Analysis</h2>
        </div>

        <div className="space-y-4">
          <div className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-primary/50 transition-colors">
            <input
              type="file"
              accept="video/*"
              onChange={handleFileChange}
              className="hidden"
              id="video-upload"
              disabled={isUploading || isAnalyzing}
            />
            <label htmlFor="video-upload" className="cursor-pointer">
              <Upload className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
              <p className="text-sm text-muted-foreground">
                {file ? (
                  <>
                    <span className="font-medium text-foreground">{file.name}</span>
                    <br />
                    {formatFileSize(file.size)}
                  </>
                ) : (
                  "Click to upload video for AI analysis"
                )}
              </p>
              <p className="text-xs text-muted-foreground mt-2">
                Videos up to 100MB (MOV, MP4, WebM)
              </p>
            </label>
          </div>

          <Button
            onClick={handleUpload}
            disabled={!file || isUploading || isAnalyzing}
            className="w-full h-12 text-lg font-semibold"
            size="lg"
          >
            {isUploading ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                Uploading...
              </>
            ) : isAnalyzing ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                Analyzing with AI...
              </>
            ) : (
              <>
                <Upload className="w-5 h-5 mr-2" />
                Upload & Analyze
              </>
            )}
          </Button>
        </div>

        {/* Analysis Results */}
        {analysis && (
          <div className="mt-6 space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="flex items-center gap-2 text-green-600">
              <CheckCircle2 className="w-5 h-5" />
              <span className="font-semibold">Analysis Complete</span>
            </div>

            <div className="grid gap-4">
              <div className="bg-muted/50 rounded-lg p-4">
                <h3 className="font-semibold mb-2 flex items-center gap-2">
                  👔 Outfit
                </h3>
                <p className="text-sm text-muted-foreground mb-2">
                  {analysis.outfit.description}
                </p>
                {analysis.outfit.items.length > 0 && (
                  <div className="flex flex-wrap gap-2">
                    {analysis.outfit.items.map((item, i) => (
                      <span
                        key={i}
                        className="text-xs bg-background px-2 py-1 rounded-full"
                      >
                        {item}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              <div className="bg-muted/50 rounded-lg p-4">
                <h3 className="font-semibold mb-2 flex items-center gap-2">
                  🎬 Activity
                </h3>
                <p className="text-sm text-muted-foreground mb-2">
                  {analysis.activity.description}
                </p>
                <div className="flex items-center gap-2 text-xs">
                  <span className="text-muted-foreground">Intensity:</span>
                  <span className="bg-background px-2 py-1 rounded-full">
                    {analysis.activity.intensity}
                  </span>
                </div>
              </div>

              <div className="bg-muted/50 rounded-lg p-4">
                <h3 className="font-semibold mb-2 flex items-center gap-2">
                  🏞️ Background
                </h3>
                <p className="text-sm text-muted-foreground mb-2">
                  {analysis.background.description}
                </p>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div>
                    <span className="text-muted-foreground">Location:</span>
                    <span className="ml-2 bg-background px-2 py-1 rounded-full">
                      {analysis.background.location_type}
                    </span>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Lighting:</span>
                    <span className="ml-2 bg-background px-2 py-1 rounded-full">
                      {analysis.background.lighting}
                    </span>
                  </div>
                </div>
              </div>

              {analysis.summary && (
                <div className="bg-primary/5 rounded-lg p-4 border border-primary/20">
                  <h3 className="font-semibold mb-2">📝 Summary</h3>
                  <p className="text-sm">{analysis.summary}</p>
                </div>
              )}
            </div>
          </div>
        )}

        {uploadedFilename && !analysis && !isAnalyzing && (
          <div className="flex items-center gap-2 text-yellow-600">
            <AlertCircle className="w-5 h-5" />
            <span className="text-sm">Analysis may take a moment to complete...</span>
          </div>
        )}
      </div>
    </Card>
  );
};

export default VideoUpload;

