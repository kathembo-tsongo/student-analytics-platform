import { Link, useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'
import { 
  LayoutDashboard, 
  Users, 
  School, 
  GraduationCap,
  BookOpen,
  UserCheck,
  BarChart3,
  Settings,
  AlertTriangle,
  FileText
} from 'lucide-react'
import { useAuthStore } from '@/store/authStore'

interface NavItem {
  title: string
  href: string
  icon: any
  roles: string[]
}

const navItems: NavItem[] = [
  {
    title: 'Dashboard',
    href: '/admin',
    icon: LayoutDashboard,
    roles: ['admin']
  },
  {
    title: 'Schools',
    href: '/admin/schools',
    icon: School,
    roles: ['admin']
  },
  {
    title: 'Users',
    href: '/admin/users',
    icon: Users,
    roles: ['admin']
  },
  {
    title: 'Analytics',
    href: '/admin/analytics',
    icon: BarChart3,
    roles: ['admin']
  },
  {
    title: 'Reports',
    href: '/admin/reports',
    icon: FileText,
    roles: ['admin']
  },
  {
    title: 'Dashboard',
    href: '/school-admin',
    icon: LayoutDashboard,
    roles: ['school_admin']
  },
  {
    title: 'Students',
    href: '/school-admin/students',
    icon: GraduationCap,
    roles: ['school_admin']
  },
  {
    title: 'Programs',
    href: '/school-admin/programs',
    icon: BookOpen,
    roles: ['school_admin']
  },
  {
    title: 'At-Risk Students',
    href: '/school-admin/at-risk',
    icon: AlertTriangle,
    roles: ['school_admin']
  },
  {
    title: 'Reports',
    href: '/school-admin/reports',
    icon: FileText,
    roles: ['school_admin']
  },
  {
    title: 'Dashboard',
    href: '/mentor',
    icon: LayoutDashboard,
    roles: ['mentor']
  },
  {
    title: 'My Students',
    href: '/mentor/students',
    icon: GraduationCap,
    roles: ['mentor']
  },
  {
    title: 'At-Risk Students',
    href: '/mentor/at-risk',
    icon: AlertTriangle,
    roles: ['mentor']
  },
  {
    title: 'Sessions',
    href: '/mentor/sessions',
    icon: UserCheck,
    roles: ['mentor']
  },
]

export default function Sidebar() {
  const location = useLocation()
  const { user } = useAuthStore()

  const filteredNavItems = navItems.filter(item => 
    user && item.roles.includes(user.role)
  )

  return (
    <div className="flex h-screen w-64 flex-col border-r bg-gradient-to-b from-slate-900 to-slate-800 text-white">
      {/* Logo */}
      <div className="flex h-16 items-center border-b border-slate-700 px-6">
        <div className="flex items-center space-x-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 shadow-lg">
            <span className="text-xl font-bold text-white">S</span>
          </div>
          <div>
            <h2 className="text-lg font-bold text-white">Strathmore</h2>
            <p className="text-xs text-slate-400">Analytics Platform</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-4">
        {filteredNavItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.href
          
          return (
            <Link
              key={item.href}
              to={item.href}
              className={cn(
                'flex items-center space-x-3 rounded-lg px-3 py-3 text-sm font-medium transition-all',
                isActive
                  ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                  : 'text-slate-300 hover:bg-slate-700 hover:text-white'
              )}
            >
              <Icon className="h-5 w-5" />
              <span>{item.title}</span>
            </Link>
          )
        })}
      </nav>

      {/* Settings */}
      <div className="border-t border-slate-700 p-3">
        <Link
          to="/settings"
          className="flex items-center space-x-3 rounded-lg px-3 py-3 text-sm font-medium text-slate-300 transition-all hover:bg-slate-700 hover:text-white"
        >
          <Settings className="h-5 w-5" />
          <span>Settings</span>
        </Link>
      </div>
    </div>
  )
}
