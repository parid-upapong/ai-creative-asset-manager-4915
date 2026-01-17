import DashboardSidebar from "@/components/layout/DashboardSidebar";
import StatsOverview from "@/components/dashboard/StatsOverview";
import UploadZone from "@/components/upload/UploadZone";

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-surface-100">
      <DashboardSidebar />
      
      <main className="ml-64 p-8 max-w-7xl mx-auto">
        <header className="flex justify-between items-end mb-8">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Creator Dashboard</h1>
            <p className="text-slate-500 mt-1">Welcome back. Your AI agents have optimized 12 assets today.</p>
          </div>
          <div className="flex gap-3">
            <button className="px-4 py-2 bg-white border border-slate-200 rounded-xl text-sm font-semibold text-slate-700 shadow-sm hover:bg-slate-50">
              Export CSV
            </button>
            <button className="px-4 py-2 bg-brand-600 rounded-xl text-sm font-semibold text-white shadow-sm hover:bg-brand-700">
              Bulk Actions
            </button>
          </div>
        </header>

        <StatsOverview />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-6">
            <section className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
              <h2 className="text-lg font-bold text-slate-900 mb-6">Asset Ingestion Pipeline</h2>
              <UploadZone />
            </section>
          </div>

          <div className="space-y-6">
            <section className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
              <h2 className="text-lg font-bold text-slate-900 mb-4">Market Readiness</h2>
              <div className="space-y-4">
                {[
                  { site: "Adobe Stock", score: 98 },
                  { site: "Shutterstock", score: 85 },
                  { site: "Getty Images", score: 92 },
                ].map((market) => (
                  <div key={market.site} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="font-medium text-slate-700">{market.site}</span>
                      <span className="text-slate-500">{market.score}%</span>
                    </div>
                    <div className="w-full bg-slate-100 h-2 rounded-full">
                      <div 
                        className="bg-brand-500 h-full rounded-full" 
                        style={{ width: `${market.score}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </section>

            <section className="bg-gradient-to-br from-brand-600 to-brand-900 p-6 rounded-3xl text-white shadow-lg">
              <h2 className="text-lg font-bold mb-2">Nexus Pro</h2>
              <p className="text-brand-100 text-sm mb-4">Unlock unlimited AI metadata generation and 4K video upscaling.</p>
              <button className="w-full py-2 bg-white text-brand-900 rounded-xl font-bold text-sm hover:bg-brand-50 transition-colors">
                Upgrade Now
              </button>
            </section>
          </div>
        </div>
      </main>
    </div>
  );
}