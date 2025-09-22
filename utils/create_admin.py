#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Utility script to create an admin user

import asyncio
import sys
import os

# Add the parent directory to Python path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import init_database
from models.user import User

async def create_admin_user():
    """Create an admin user for dashboard access"""
    try:
        # Initialize database
        await init_database()
        print("✅ Database connection established")
        
        # Check if admin user already exists
        existing_admin = await User.find_by_username('admin')
        if existing_admin:
            print("⚠️  Admin user already exists!")
            print(f"   Username: {existing_admin.username}")
            print(f"   Email: {existing_admin.email}")
            print(f"   Role: {existing_admin.role}")
            print(f"   Is Admin: {existing_admin.is_admin}")
            return
        
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@hersel.it',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        
        # Set password (change this to a secure password)
        admin_password = 'admin123'  # CHANGE THIS IN PRODUCTION!
        admin_user.set_password(admin_password)
        
        # Save user
        await admin_user.save()
        
        print("🎉 Admin user created successfully!")
        print("📝 Login credentials:")
        print(f"   Username: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   Password: {admin_password}")
        print(f"   Role: {admin_user.role}")
        print(f"   Is Admin: {admin_user.is_admin}")
        print("")
        print("🔐 IMPORTANT: Change the default password after first login!")
        print("📍 You can now access the dashboard at: /dashboard/")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        import traceback
        traceback.print_exc()

async def list_users():
    """List all users in the system"""
    try:
        await init_database()
        users = await User.get_all()
        
        if not users:
            print("No users found in the system.")
            return
        
        print("\n👥 Users in the system:")
        print("-" * 80)
        print(f"{'ID':<5} {'Username':<15} {'Email':<25} {'Role':<10} {'Admin':<7} {'Active':<8}")
        print("-" * 80)
        
        for user in users:
            print(f"{user.id:<5} {user.username:<15} {user.email:<25} {user.role:<10} {user.is_admin:<7} {user.is_active:<8}")
        
        print("-" * 80)
        print(f"Total users: {len(users)}")
        
    except Exception as e:
        print(f"❌ Error listing users: {e}")

async def promote_user_to_admin(username):
    """Promote an existing user to admin"""
    try:
        await init_database()
        user = await User.find_by_username(username)
        
        if not user:
            print(f"❌ User '{username}' not found.")
            return
        
        # Update user role
        user.role = 'admin'
        await user.save()
        
        print(f"✅ User '{username}' promoted to admin successfully!")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Role: {user.role}")
        print(f"   Is Admin: {user.is_admin}")
        
    except Exception as e:
        print(f"❌ Error promoting user: {e}")

def print_usage():
    """Print usage instructions"""
    print("Usage:")
    print("  python utils/create_admin.py create       # Create default admin user")
    print("  python utils/create_admin.py list         # List all users")
    print("  python utils/create_admin.py promote <username>  # Promote user to admin")
    print("")
    print("Examples:")
    print("  python utils/create_admin.py create")
    print("  python utils/create_admin.py promote john_doe")

async def main():
    """Main function"""
    if len(sys.argv) < 2:
        print_usage()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'create':
        await create_admin_user()
    elif command == 'list':
        await list_users()
    elif command == 'promote':
        if len(sys.argv) < 3:
            print("❌ Please provide a username to promote.")
            print("   Usage: python utils/create_admin.py promote <username>")
            return
        username = sys.argv[2]
        await promote_user_to_admin(username)
    else:
        print(f"❌ Unknown command: {command}")
        print_usage()

if __name__ == '__main__':
    asyncio.run(main())