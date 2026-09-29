using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Security.Claims;
using VendorDirectory.API.Data;
using VendorDirectory.API.DTOs;
using VendorDirectory.API.Models;

namespace VendorDirectory.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize] // All endpoints require authentication
    public class VendorsController : ControllerBase
    {
        private readonly ApplicationDbContext _context;

        public VendorsController(ApplicationDbContext context)
        {
            _context = context;
        }

        // GET: api/vendors
        [HttpGet]
        public async Task<IActionResult> GetVendors(
            [FromQuery] string? search,
            [FromQuery] string? status,
            [FromQuery] string? category)
        {
            var query = _context.Vendors.AsQueryable();

            // Apply filters
            if (!string.IsNullOrWhiteSpace(search))
            {
                query = query.Where(v =>
                    v.VendorName.Contains(search) ||
                    (v.ContactPerson != null && v.ContactPerson.Contains(search)) ||
                    (v.Email != null && v.Email.Contains(search)));
            }

            if (!string.IsNullOrWhiteSpace(status))
            {
                query = query.Where(v => v.Status == status);
            }

            if (!string.IsNullOrWhiteSpace(category))
            {
                query = query.Where(v => v.Category == category);
            }

            var vendors = await query
                .OrderBy(v => v.VendorName)
                .Select(v => new VendorDto
                {
                    Id = v.Id,
                    VendorName = v.VendorName,
                    ContactPerson = v.ContactPerson,
                    Email = v.Email,
                    Phone = v.Phone,
                    Street = v.Street,
                    City = v.City,
                    State = v.State,
                    ZipCode = v.ZipCode,
                    Country = v.Country,
                    Status = v.Status,
                    Category = v.Category,
                    Notes = v.Notes,
                    CreatedAt = v.CreatedAt,
                    UpdatedAt = v.UpdatedAt
                })
                .ToListAsync();

            return Ok(vendors);
        }

        // GET: api/vendors/{id}
        [HttpGet("{id}")]
        public async Task<IActionResult> GetVendor(int id)
        {
            var vendor = await _context.Vendors.FindAsync(id);

            if (vendor == null)
            {
                return NotFound(new { message = "Vendor not found" });
            }

            var vendorDto = new VendorDto
            {
                Id = vendor.Id,
                VendorName = vendor.VendorName,
                ContactPerson = vendor.ContactPerson,
                Email = vendor.Email,
                Phone = vendor.Phone,
                Street = vendor.Street,
                City = vendor.City,
                State = vendor.State,
                ZipCode = vendor.ZipCode,
                Country = vendor.Country,
                Status = vendor.Status,
                Category = vendor.Category,
                Notes = vendor.Notes,
                CreatedAt = vendor.CreatedAt,
                UpdatedAt = vendor.UpdatedAt
            };

            return Ok(vendorDto);
        }

        // POST: api/vendors (Admin only)
        [HttpPost]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> CreateVendor([FromBody] CreateVendorRequest request)
        {
            var userIdClaim = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            if (userIdClaim == null)
            {
                return Unauthorized();
            }

            var vendor = new Vendor
            {
                VendorName = request.VendorName,
                ContactPerson = request.ContactPerson,
                Email = request.Email,
                Phone = request.Phone,
                Street = request.Street,
                City = request.City,
                State = request.State,
                ZipCode = request.ZipCode,
                Country = request.Country,
                Status = request.Status,
                Category = request.Category,
                Notes = request.Notes,
                CreatedBy = int.Parse(userIdClaim)
            };

            _context.Vendors.Add(vendor);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetVendor), new { id = vendor.Id }, new VendorDto
            {
                Id = vendor.Id,
                VendorName = vendor.VendorName,
                ContactPerson = vendor.ContactPerson,
                Email = vendor.Email,
                Phone = vendor.Phone,
                Street = vendor.Street,
                City = vendor.City,
                State = vendor.State,
                ZipCode = vendor.ZipCode,
                Country = vendor.Country,
                Status = vendor.Status,
                Category = vendor.Category,
                Notes = vendor.Notes,
                CreatedAt = vendor.CreatedAt,
                UpdatedAt = vendor.UpdatedAt
            });
        }

        // PUT: api/vendors/{id} (Admin only)
        [HttpPut("{id}")]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> UpdateVendor(int id, [FromBody] UpdateVendorRequest request)
        {
            var vendor = await _context.Vendors.FindAsync(id);

            if (vendor == null)
            {
                return NotFound(new { message = "Vendor not found" });
            }

            // Update vendor properties
            vendor.VendorName = request.VendorName;
            vendor.ContactPerson = request.ContactPerson;
            vendor.Email = request.Email;
            vendor.Phone = request.Phone;
            vendor.Street = request.Street;
            vendor.City = request.City;
            vendor.State = request.State;
            vendor.ZipCode = request.ZipCode;
            vendor.Country = request.Country;
            vendor.Status = request.Status;
            vendor.Category = request.Category;
            vendor.Notes = request.Notes;
            vendor.UpdatedAt = DateTime.UtcNow;

            await _context.SaveChangesAsync();

            return Ok(new VendorDto
            {
                Id = vendor.Id,
                VendorName = vendor.VendorName,
                ContactPerson = vendor.ContactPerson,
                Email = vendor.Email,
                Phone = vendor.Phone,
                Street = vendor.Street,
                City = vendor.City,
                State = vendor.State,
                ZipCode = vendor.ZipCode,
                Country = vendor.Country,
                Status = vendor.Status,
                Category = vendor.Category,
                Notes = vendor.Notes,
                CreatedAt = vendor.CreatedAt,
                UpdatedAt = vendor.UpdatedAt
            });
        }

        // DELETE: api/vendors/{id} (Admin only)
        [HttpDelete("{id}")]
        [Authorize(Roles = "Admin")]
        public async Task<IActionResult> DeleteVendor(int id)
        {
            var vendor = await _context.Vendors.FindAsync(id);

            if (vendor == null)
            {
                return NotFound(new { message = "Vendor not found" });
            }

            _context.Vendors.Remove(vendor);
            await _context.SaveChangesAsync();

            return Ok(new { message = "Vendor deleted successfully" });
        }
    }
}
