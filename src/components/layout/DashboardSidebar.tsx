import { LayoutDashboard, Image as ImageIcon, Sparkles, Settings, BarChart, LogOut } from "lucide-react";
import Link from "next/link";

const menuItems = [
  { icon: LayoutDashboard, label: "Overview", href: "/dashboard", active: true },
  { icon: ImageIcon, label: "My Library", href: "/library" },
  { icon: Sparkles, label: "AI Enhancer", href: "/ai" },
  { icon: BarChart, label: "Analytics", href: "/analytics" },
  { icon: Settings, label: "Settings", href: "/settings" },
];

export default function DashboardSidebar() {
  return (
    <aside className="w-64 h-screen border-r border-slate-200 bg-surface-50 flex flex-col p-6 fixed left-0 top-0">
      <div className="flex items-center gap-2 mb-10 px-2">
        <div className="w-8 h-8 bg-brand-600 rounded-lg flex items-center justify-center">
          <Sparkles className="text-white w-5 h-5" />
        </div>
        <span className="text-xl font-bold tracking-tight text-slate-900">Nexus AI</span>
      </div>

      <nav className="flex-1 space-y-1">
        {menuItems.map((item) => (
          <Link
            key={item.label}
            href={item.href}
            className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-colors ${
              item.active ? "bg-brand-50 text-brand-600" : "text-slate-600 hover:bg-slate-50"
            }`}
          >
            <item.icon className="w-5 h-5" />
            {item.label}
          </Link>
        ))}
      </nav>

      <div className="pt-6 border-t border-slate-200">
        <button className="flex items-center gap-3 px-3 py-2.5 w-full text-sm font-medium text-slate-600 hover:text-red-600 transition-colors">
          <LogOut className="w-5 h-5" />
          Logout
        </button>
      </div>
    </aside>
  );
}