import { Card } from "@/components/ui/card";
import { Briefcase, GraduationCap, Lightbulb, Users } from "lucide-react";

type PostType = "performative" | "serious" | "cluely" | "boardy";

interface PostTypeSelectorProps {
  value: PostType;
  onChange: (value: PostType) => void;
}

const postTypes = [
  {
    id: "performative" as PostType,
    title: "Performative",
    description: "Humble brags and virtue signaling",
    icon: Briefcase,
    gradient: "from-primary/20 to-primary/5",
  },
  {
    id: "serious" as PostType,
    title: "Serious",
    description: "Corporate jargon overload",
    icon: GraduationCap,
    gradient: "from-accent/20 to-accent/5",
  },
  {
    id: "cluely" as PostType,
    title: "Cluely",
    description: "Out of touch with reality",
    icon: Lightbulb,
    gradient: "from-muted to-muted/50",
  },
  {
    id: "boardy" as PostType,
    title: "Boardy",
    description: "Excessive meeting culture vibes",
    icon: Users,
    gradient: "from-primary/15 to-accent/10",
  },
];

const PostTypeSelector = ({ value, onChange }: PostTypeSelectorProps) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {postTypes.map((type) => {
        const Icon = type.icon;
        const isSelected = value === type.id;
        
        return (
          <Card
            key={type.id}
            className={`p-6 cursor-pointer transition-all hover:scale-105 ${
              isSelected
                ? "ring-2 ring-primary shadow-lg bg-gradient-to-br " + type.gradient
                : "hover:shadow-md"
            }`}
            onClick={() => onChange(type.id)}
          >
            <div className="flex flex-col items-center text-center space-y-3">
              <div
                className={`w-12 h-12 rounded-full flex items-center justify-center ${
                  isSelected ? "bg-primary text-primary-foreground" : "bg-muted"
                }`}
              >
                <Icon className="w-6 h-6" />
              </div>
              <div>
                <h3 className="font-semibold text-lg">{type.title}</h3>
                <p className="text-sm text-muted-foreground mt-1">{type.description}</p>
              </div>
            </div>
          </Card>
        );
      })}
    </div>
  );
};

export default PostTypeSelector;
