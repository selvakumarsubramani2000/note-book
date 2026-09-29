using System.ComponentModel.DataAnnotations;

namespace VendorDirectory.API.Models
{
    public class User
    {
        public int Id { get; set; }

        [Required]
        [EmailAddress]
        public string Email { get; set; } = string.Empty;

        [Required]
        public string PasswordHash { get; set; } = string.Empty;

        [Required]
        public string Name { get; set; } = string.Empty;

        public string Role { get; set; } = "User"; // Default role: User or Admin

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    }
}

