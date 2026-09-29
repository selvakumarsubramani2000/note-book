using System.ComponentModel.DataAnnotations;

namespace VendorDirectory.API.Models
{
    public class Vendor
    {
        public int Id { get; set; }

        [Required]
        [StringLength(200)]
        public string VendorName { get; set; } = string.Empty;

        [StringLength(100)]
        public string? ContactPerson { get; set; }

        [EmailAddress]
        [StringLength(255)]
        public string? Email { get; set; }

        [StringLength(50)]
        public string? Phone { get; set; }

        [StringLength(200)]
        public string? Street { get; set; }

        [StringLength(100)]
        public string? City { get; set; }

        [StringLength(50)]
        public string? State { get; set; }

        [StringLength(20)]
        public string? ZipCode { get; set; }

        [StringLength(100)]
        public string? Country { get; set; }

        [Required]
        [StringLength(20)]
        public string Status { get; set; } = "Active"; // Active or Inactive

        [StringLength(50)]
        public string? Category { get; set; } // Supplier, Manufacturer, Distributor

        public string? Notes { get; set; }

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        public DateTime? UpdatedAt { get; set; }

        public int? CreatedBy { get; set; } // Foreign key to User
    }
}

