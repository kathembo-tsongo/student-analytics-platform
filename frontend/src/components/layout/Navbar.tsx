import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { useAuthStore } from '@/store/authStore'
import { logout as apiLogout } from '@/services/api'
import { 
  LogOut, 
  User, 
  Bell, 
  Search,
  Menu,
  ChevronDown,
  Settings,
  HelpCircle
} from 'lucide-react'

interface NavbarProps {
  onMenuClick?: () => void
}

export default function Navbar({ onMenuClick }: NavbarProps) {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()
  const [showUserMenu, setShowUserMenu] = useState(false)

  const handleLogout = async () => {
    try {
      await apiLogout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      logout()
      navigate('/login')
    }
  }

  const getRoleName = (role: string) => {
    const roleNames: Record<string, string> = {
      admin: 'System Administrator',
      school_admin: 'School Administrator',
      mentor: 'Mentor'
    }
    return roleNames[role] || role
  }

  const getRoleColor = (role: string) => {
    const colors: Record<string, string> = {
      admin: 'from-blue-500 to-purple-600',
      school_admin: 'from-purple-500 to-pink-600',
      mentor: 'from-green-500 to-emerald-600'
    }
    return colors[role] || 'from-gray-500 to-gray-600'
  }

  return (
    <header className="sticky top-0 z-40 border-b border-gray-200 bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/80">
      <div className="flex h-16 items-center px-4 lg:px-6">
        <div className="flex flex-1 items-center space-x-4">
          {/* Mobile Menu Button */}
          <button
            onClick={onMenuClick}
            className="lg:hidden rounded-lg p-2 transition-colors hover:bg-gray-100 active:bg-gray-200"
          >
            <Menu className="h-6 w-6 text-gray-600" />
          </button>

          {/* Search Bar */}
          <div className="hidden md:flex flex-1 max-w-xl">
            <div className="relative w-full group">
              <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400 transition-colors group-focus-within:text-blue-600" />
              <input
                type="text"
                placeholder="Search students, programs, schools..."
                className="h-11 w-full rounded-xl border-2 border-gray-200 bg-gray-50 pl-12 pr-4 text-sm font-medium text-gray-900 placeholder:text-gray-400 transition-all focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500/20"
              />
              <kbd className="absolute right-4 top-1/2 -translate-y-1/2 rounded bg-gray-200 px-2 py-1 text-xs font-semibold text-gray-600 hidden lg:inline-block">
                ⌘K
              </kbd>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          {/* Quick Actions */}
          <button className="hidden md:flex items-center space-x-2 rounded-lg px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-100">
            <HelpCircle className="h-4 w-4" />
            <span>Help</span>
          </button>

          {/* Notifications */}
          <button className="relative rounded-lg p-2.5 transition-all hover:bg-gray-100 active:scale-95">
            <Bell className="h-5 w-5 text-gray-600" />
            <span className="absolute right-1.5 top-1.5 flex h-4 w-4 items-center justify-center rounded-full bg-gradient-to-br from-red-500 to-pink-600 text-[10px] font-bold text-white shadow-lg">
              3
            </span>
            <span className="absolute right-1.5 top-1.5 h-4 w-4 animate-ping rounded-full bg-red-400 opacity-75"></span>
          </button>

          {/* User Menu */}
          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center space-x-3 rounded-xl px-3 py-2 transition-all hover:bg-gray-100 active:scale-95"
            >
              <div className={`flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br ${user && getRoleColor(user.role)} shadow-lg transition-transform hover:scale-105`}>
                <span className="text-sm font-bold text-white">
                  {user?.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)}
                </span>
              </div>
              <div className="hidden text-left lg:block">
                <p className="text-sm font-semibold text-gray-900">{user?.name}</p>
                <p className="text-xs text-gray-500">{user && getRoleName(user.role)}</p>
              </div>
              <ChevronDown className={`h-4 w-4 text-gray-400 transition-transform ${showUserMenu ? 'rotate-180' : ''}`} />
            </button>

            {/* Dropdown Menu */}
            {showUserMenu && (
              <>
                <div
                  className="fixed inset-0 z-10"
                  onClick={() => setShowUserMenu(false)}
                ></div>
                <div className="absolute right-0 z-20 mt-2 w-72 rounded-xl border border-gray-200 bg-white shadow-2xl animate-in fade-in slide-in-from-top-2">
                  {/* User Info Header */}
                  <div className={`rounded-t-xl bg-gradient-to-br ${user && getRoleColor(user.role)} p-4`}>
                    <div className="flex items-center space-x-3">
                      <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-white/20 backdrop-blur-sm">
                        <span className="text-lg font-bold text-white">
                          {user?.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)}
                        </span>
                      </div>
                      <div className="flex-1">
                        <p className="font-semibold text-white">{user?.name}</p>
                        <p className="text-sm text-white/80">{user?.email}</p>
                      </div>
                    </div>
                    <div className="mt-3 inline-flex rounded-full bg-white/20 px-3 py-1 backdrop-blur-sm">
                      <span className="text-xs font-medium text-white">
                        {user && getRoleName(user.role)}
                      </span>
                    </div>
                  </div>

                  {/* Menu Items */}
                  <div className="p-2">
                    <button
                      onClick={() => {
                        setShowUserMenu(false)
                        navigate('/profile')
                      }}
                      className="flex w-full items-center space-x-3 rounded-lg px-4 py-3 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-100"
                    >
                      <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-50">
                        <User className="h-4 w-4 text-blue-600" />
                      </div>
                      <div className="flex-1 text-left">
                        <p className="font-medium">Profile</p>
                        <p className="text-xs text-gray-500">View and edit profile</p>
                      </div>
                    </button>

                    <button
                      onClick={() => {
                        setShowUserMenu(false)
                        navigate('/settings')
                      }}
                      className="flex w-full items-center space-x-3 rounded-lg px-4 py-3 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-100"
                    >
                      <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-purple-50">
                        <Settings className="h-4 w-4 text-purple-600" />
                      </div>
                      <div className="flex-1 text-left">
                        <p className="font-medium">Settings</p>
                        <p className="text-xs text-gray-500">Preferences & privacy</p>
                      </div>
                    </button>

                    <div className="my-2 border-t border-gray-200"></div>

                    <button
                      onClick={handleLogout}
                      className="flex w-full items-center space-x-3 rounded-lg px-4 py-3 text-sm font-medium text-red-600 transition-colors hover:bg-red-50"
                    >
                      <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-red-50">
                        <LogOut className="h-4 w-4 text-red-600" />
                      </div>
                      <div className="flex-1 text-left">
                        <p className="font-medium">Logout</p>
                        <p className="text-xs text-red-500">Sign out of your account</p>
                      </div>
                    </button>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}
