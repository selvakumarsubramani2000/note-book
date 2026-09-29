using System.ComponentModel.DataAnnotations;

namespace VendorDirectory.API.DTOs
{
    public class VendorDto
    {
        public int Id { get; set; }
        public string VendorName { get; set; } = string.Empty;
        public string? ContactPerson { get; set; }
        public string? Email { get; set; }
        public string? Phone { get; set; }
        public string? Street { get; set; }
        public string? City { get; set; }
        public string? State { get; set; }
        public string? ZipCode { get; set; }
        public string? Country { get; set; }
        public string Status { get; set; } = string.Empty;
        public string? Category { get; set; }
        public string? Notes { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime? UpdatedAt { get; set; }
    }

    public class CreateVendorRequest
    {
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
        public string Status { get; set; } = "Active";

        [StringLength(50)]
        public string? Category { get; set; }

        public string? Notes { get; set; }
    }

    public class UpdateVendorRequest
    {
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
        public string Status { get; set; } = "Active";

        [StringLength(50)]
        public string? Category { get; set; }

        public string? Notes { get; set; }
    }
}

