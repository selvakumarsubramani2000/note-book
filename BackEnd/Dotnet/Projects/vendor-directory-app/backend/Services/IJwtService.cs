using VendorDirectory.API.Models;

namespace VendorDirectory.API.Services
{
    public interface IJwtService
    {
        string GenerateToken(User user);
    }
}

