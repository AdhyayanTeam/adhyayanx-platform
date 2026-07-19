"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/features/auth";
import { Button } from "@/shared/ui/button";
import { LoadingSpinner } from "@/shared/ui/loading-spinner";
import { cn } from "@/shared/lib/utils";
import {
  Calendar,
  BookOpen,
  UserPlus,
  Users,
  LayoutList,
  Radio,
  User,
  Building2,
  Settings,
  LogOut,
} from "lucide-react";

interface NavItem {
  href: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
}

interface NavGroup {
  label: string;
  items: NavItem[];
}

const navGroups: NavGroup[] = [
  {
    label: "Academy",
    items: [
      { href: "/academy/today", label: "Today's Classes", icon: Calendar },
      { href: "/academy/catalog", label: "Catalog", icon: BookOpen },
      { href: "/academy/admissions", label: "Admissions", icon: UserPlus },
      { href: "/academy/students", label: "Students", icon: Users },
    ],
  },
  {
    label: "Account",
    items: [
      { href: "/console/profile", label: "Profile", icon: User },
      { href: "/console/organization", label: "Organization", icon: Building2 },
      { href: "/console/settings", label: "Settings", icon: Settings },
    ],
  },
];

function isActive(pathname: string, href: string) {
  if (href === "/academy/today") return pathname === "/academy/today";
  return pathname === href || pathname.startsWith(href + "/");
}

export function ConsoleSidebar() {
  const pathname = usePathname();
  const { user, organization, isLoading, logout } = useAuth();

  if (isLoading) {
    return (
      <aside className="w-64 border-r p-4 flex items-center justify-center">
        <LoadingSpinner />
      </aside>
    );
  }

  return (
    <aside className="w-64 border-r p-4 flex flex-col h-screen sticky top-0">
      <div className="mb-6">
        <h1 className="text-lg font-bold">ADX Platform</h1>
        {organization && (
          <p className="text-sm text-muted-foreground truncate">{organization.name}</p>
        )}
      </div>

      <nav className="flex-1 space-y-5 overflow-y-auto">
        {navGroups.map((group) => (
          <div key={group.label}>
            <p className="text-xs font-semibold uppercase text-muted-foreground tracking-wider mb-2 px-1">
              {group.label}
            </p>
            <div className="space-y-0.5">
              {group.items.map((item) => {
                const active = isActive(pathname, item.href);
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={cn(
                      "flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors",
                      active
                        ? "bg-secondary text-secondary-foreground font-medium"
                        : "text-muted-foreground hover:bg-secondary/50 hover:text-secondary-foreground"
                    )}
                  >
                    <item.icon className="h-4 w-4" />
                    {item.label}
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </nav>

      <div className="border-t pt-4 mt-4">
        <div className="text-sm mb-2">
          <p className="font-medium truncate">{user?.name}</p>
          <p className="text-muted-foreground truncate">{user?.email}</p>
        </div>
        <Button variant="ghost" size="sm" className="w-full justify-start" onClick={logout}>
          <LogOut className="h-4 w-4 mr-2" />
          Log out
        </Button>
      </div>
    </aside>
  );
}
