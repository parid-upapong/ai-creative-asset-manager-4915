import { BarChart3, CloudUpload, Sparkles, TrendingUp } from "lucide-react";

const stats = [
  { label: "Total Assets", value: "1,284", icon: CloudUpload, change: "+12%" },
  { label: "AI Hours Saved", value: "142h", icon: Sparkles, change: "+18%" },
  { label: "Market Revenue", value: "$3,420", icon: TrendingUp, change: "+5.4%" },
  { label: "Optimization Score", value: "94%", icon: BarChart3, change: "+2%" },
];

export default function StatsOverview() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      {stats.map((stat) => (
        <div key={stat.label} className="p-6 bg-white border border-slate-200 rounded-2xl shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div className="p-2 bg-brand-50 rounded-lg">
              <stat.icon className="w-5 h-5 text-brand-600" />
            </div>
            <span className="text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full">
              {stat.change}
            </span>
          </div>
          <p className="text-sm text-slate-500 font-medium">{stat.label}</p>
          <h3 className="text-2xl font-bold text-slate-900">{stat.value}</h3>
        </div>
      ))}
    </div>
  );
}