# Telegram Video Bot

A powerful Telegram bot for managing and sharing video content with premium features and daily limits.

## Features

### Free User Features
- Limited daily file processing
- Video length restricted to 5 minutes
- Basic access to public content

### Premium User Features
- Increased daily file processing limit
- Unlimited video length support
- Access to premium content
- Priority support

## Subscription Plans (INR)

- **Weekly Plan**: ₹20
- **Fortnightly Plan**: ₹30
- **Monthly Plan**: ₹50

## User Commands

- `/start` - Start the bot
- `/plans` - View available subscription plans
- `/myplan` - Check your current plan details including:
  - Current plan status
  - Daily limit and usage
  - Subscription expiry (for premium users)
  - Remaining quota

## Admin Commands

- `/stats` - View bot statistics (total users, active users, files)
- `/broadcast` - Send message to all users
- `/ban` - Ban a user from using the bot
- `/unban` - Unban a previously banned user
- `/maintenance` - Toggle maintenance mode
- `/add` - Add premium access for a user
- `/remove` - Remove premium access from a user
- `/setlimit` - Set daily limits for free/premium users
- `/deleteall` - Delete all videos from database
- `/delete` - Delete specific video by ID

## Bot Source Code

### Features Included
- User management system
- Premium subscription handling
- File processing capabilities
- Admin control panel
- Broadcast system
- Maintenance mode
- Daily usage tracking
- Premium content access control

### Technical Specifications
- Built with Pyrogram
- Database integration
- Timezone support (IST)
- Automated expiry management
- User activity tracking

## Support

For support or premium plan activation, contact the admin through Telegram.

## Note

This bot includes a complete backend system for managing users, subscriptions, and content. The pricing includes the full source code with all features mentioned above.
