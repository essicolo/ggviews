class TestCoordinateSystems:
    """Test coordinate systems"""
    
    def test_coord_fixed(self, sample_data):
        """Test coord_fixed"""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + coord_fixed())
        
        assert p.coord_system is not None
        assert hasattr(p.coord_system, 'ratio')
        assert p.coord_system.ratio == 1
    
    def test_coord_fixed_custom_ratio(self, sample_data):
        """Test coord_fixed with custom ratio"""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + coord_fixed(ratio=2))
        
        assert p.coord_system is not None
        assert p.coord_system.ratio == 2
    
    def test_coord_equal(self, sample_data):
        """Test coord_equal"""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + coord_equal())
        
        assert p.coord_system is not None
        assert p.coord_system.ratio == 1
    
    def test_coord_flip(self, sample_data):
        """Test coord_flip"""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + coord_flip())
        
        assert p.coord_system is not None
        assert hasattr(p.coord_system, '_apply')

    def test_chaining_coord_fixed(self, sample_data):
        """Test chaining coord_fixed method"""
        p = ggplot(sample_data, aes(x='x', y='y')).geom_point().coord_fixed()
        assert p.coord_system is not None
        assert p.coord_system.ratio == 1
    
    def test_chaining_coord_equal(self, sample_data):
        """Test chaining coord_equal method"""
        p = ggplot(sample_data, aes(x='x', y='y')).geom_point().coord_equal()
        assert p.coord_system is not None
        assert p.coord_system.ratio == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
